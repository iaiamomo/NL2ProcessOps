from langchain.schema.runnable import Runnable, RunnableLambda, RunnablePassthrough, RunnableBranch
from TasksModelLLM import MermaidLLM
from TasksPreProcessingLLM import TaskRetrieverLLM
from CodeLLM import CodeLLM
from DeployLLM import DeployLLM
from ToolsManagerDB import ToolStore
from langchain_openai import OpenAIEmbeddings
import ast
import json
import os
import dotenv
import glob
import pandas as pd
from io import StringIO
import tokenize


class ProcessLLM:

    def __init__(self, model="gpt-3.5-turbo", openai_key=None, temperature=0.0):
        self.model_tasks_llm = MermaidLLM(model, openai_key, temperature=temperature)
        self.task_llm = TaskRetrieverLLM(model, openai_key, temperature=temperature)
        self.code_llm = CodeLLM(model, openai_key, temperature=temperature)
        self.deploy_llm = DeployLLM(model, openai_key, temperature=temperature)

        embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=openai_key)
        self.tools_store = ToolStore(openai_key)
        self.tools_store.embed_tools(embedding_function)


    def tools_prompt_parser(self, task_llm_output: dict) -> str:
        """Retrieve the list of tools from the tasks list"""
        tool_list = ""
        task_list = ast.literal_eval(task_llm_output)
        for task in task_list:
            # retrieve the tool
            res = self.tools_store.search(task)['output']
            if res == []:
                continue
            else:
                for elem in res:
                    tool_desc = {
                        "name": elem["name"],
                        "description": elem["description"],
                        "input_parameters": elem["input_parameters"],
                        "output_parameters": elem["output_parameters"],
                        "actor": elem["actor"]
                    }
                    tool_desc_str = json.dumps(tool_desc)
                    if tool_desc_str not in tool_list:
                        tool_list += f"{json.dumps(tool_desc)}\n"
                    print(f"task: {task} tool: {elem['name']}")

        print(f"Tools: {tool_list}")

        return tool_list


    def is_list_of_tasks(self, output: str) -> bool:
        """Check if the output from the task retriever is a list of tasks"""
        # convert a string to list
        try:
            result_list = ast.literal_eval(output)
            if not isinstance(result_list, list):
                return []
        except:
            result_list = []
        if len(result_list) == 0:
            return False
        
        print(f"Tasks: {result_list}")
        
        return True


    def remove_comments_and_docstrings(self, source):
        io_obj = StringIO(source)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
            # Remove comments:
            if token_type == tokenize.COMMENT:
                pass
            # This series of conditionals removes docstrings:
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
            # This is likely a docstring; double-check we're not inside an operator:
                    if prev_toktype != tokenize.NEWLINE:
                        if start_col > 0:
                            out += token_string
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
        temp=[]
        for x in out.split('\n'):
            if x.strip()!="":
                temp.append(x)
        return '\n'.join(temp)


    def deploy_llm_parser(self) -> Runnable:
        deploy_llm_chain = self.deploy_llm.get_chain()

        deploy_llm_chain_output = {
            "code_r": deploy_llm_chain,
            "inputs": RunnablePassthrough()
        }

        deploy_llm_chain_output = (
            RunnableLambda(lambda x: {
                "input": x["inputs"]["input"],
                "tools": x["inputs"]["tools"],
                "model": x["inputs"]["model"],
                "tasks": x["inputs"]["tasks"],
                "original_tasks": x["inputs"]["original_tasks"],
                "code": x["inputs"]["code"],
                "code_r": self.remove_comments_and_docstrings(x["inputs"]["code"])
                })
            | deploy_llm_chain_output
            | RunnableLambda(lambda x: {
                "code_r": x["code_r"],
                "input": x["inputs"]["input"],
                "tools": x["inputs"]["tools"],
                "model": x["inputs"]["model"],
                "tasks": x["inputs"]["tasks"],
                "original_tasks": x["inputs"]["original_tasks"],
                "code": x["inputs"]["code"]
                })
        )

        return deploy_llm_chain_output



    def save_code(self, output_chain) -> Runnable:
        error_python = False

        try:
            tools = output_chain["tools"]
            tools_list = tools.split("}\n")

            py_file = ""

            # import all the used tools
            for elem in range(len(tools_list)-1):
                tool_str = tools_list[elem] + "}"
                tool = json.loads(tool_str)

                module = tool["actor"]
                class_name = tool["name"]
                py_file += f"from tools.{module} import {class_name}\n"
            
            # add the python function
            py_file += "\n"
            py_file += output_chain["code"]

            # TODO: check if the function is called with the right parameters
            # TODO: check if the function is called and call it otherwise
            # get the function name
            '''function_name = ""
            tree = ast.parse(py_file)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_name = node.name
            # check if the function is called and call it otherwise
            lines_py_file = py_file.strip("\n").split("\n")
            if function_name not in lines_py_file[-1]:
                py_file += f"\n\nif __name__ == '__main__':\n\t{function_name}()"'''

            with open("llm_process_code.py", "w+") as f:
                f.write(py_file)
        except Exception as e:
            print(e)
            error_python = True

        json_output = {
            "tools": output_chain["tools"],
            "code": output_chain["code"],
            "input": output_chain["input"],
            "model": output_chain["model"],
            "tasks": output_chain["tasks"],
            "original_tasks": output_chain["original_tasks"],
            "error_python": error_python
        }
        
        return json_output


    def code_llm_parser(self) -> Runnable:
        code_llm_chain = self.code_llm.get_chain()

        code_llm_chain_output = {
            "code": code_llm_chain,
            "inputs": RunnablePassthrough()
        }

        code_llm_chain_output = (
            code_llm_chain_output
            | RunnableLambda(lambda x: {
                "code": x["code"],
                "input": x["inputs"]["input"],
                "tools": x["inputs"]["tools"],
                "model": x["inputs"]["model"],
                "tasks": x["inputs"]["tasks"],
                "original_tasks": x["inputs"]["original_tasks"]
                })
            | RunnableLambda(lambda x: self.save_code(x))
        )

        return code_llm_chain_output


    def task_llm_parser(self) -> Runnable:
        task_llm_chain = self.task_llm.get_chain()

        task_llm_chain_output = {
            "tasks": task_llm_chain,
            "inputs": RunnablePassthrough()
        }

        task_llm_chain_output = (
            task_llm_chain_output
            | RunnableLambda(lambda x: {
                "tasks": x["tasks"],
                "input": x["inputs"]["input"],
                "model": x["inputs"]["model"],
                "original_tasks": x["inputs"]["tasks"]
                })
        )

        return task_llm_chain_output


    def model_tasks_llm_parser(self) -> Runnable:
        model_llm_chain = self.model_tasks_llm.get_chain()

        model_llm_chain_output = {
            "output": model_llm_chain,
            "inputs": RunnablePassthrough()
        }

        model_llm_chain_output = (
            model_llm_chain_output
            | RunnableLambda(lambda x: {
                "model": x["output"]["model"],
                "tasks": x["output"]["tasks"],
                "input": x["inputs"]["input"]
                })
        )

        return model_llm_chain_output

    def parse_output(self, output_chain: dict) -> str:
        out_txt = f"Python code:\n{output_chain['code']}"
        return out_txt

    def get_chain(self):
        model_tasks_llm_chain_output = self.model_tasks_llm_parser()
        task_llm_chain_output = self.task_llm_parser()
        code_llm_chain_output = self.code_llm_parser()
        deploy_llm_chain_output = self.deploy_llm.get_chain()

        # general chain that takes as input the process description, the model and the tools
        # it executes only if there are tasks in the process description
        general_chain = (
            RunnableLambda(lambda x: {
                "model": x["model"],
                "tools": self.tools_prompt_parser(x["tasks"]),
                "input": x["input"],
                "tasks": x["tasks"],
                "original_tasks": x["original_tasks"]
                })
            | code_llm_chain_output
            | RunnableBranch(
                (lambda x: not x["error_python"], RunnableLambda(lambda x: {
                    deploy_llm_chain_output,
                })),
                (lambda x: "There are some errors in the python code.")
            )
        )

        chain = (
            model_tasks_llm_chain_output
            | task_llm_chain_output
            | RunnableLambda(
                lambda x: {
                    "tasks": x["tasks"],
                    "has_tasks": self.is_list_of_tasks(x["tasks"]),
                    "original_tasks": x["original_tasks"],
                    "input": x["input"],
                    "model": x["model"]
                }
            )
            | RunnableBranch(
                (lambda x: x["has_tasks"], general_chain),
                (lambda x: "Your process description does not contain any task.")
            )
        )

        return chain


if __name__ == "__main__":
    dotenv.load_dotenv("exe.env")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    models = ["gpt-4-0125-preview"]
    
    processes = glob.glob("../eval_code/data/*")
    processes = [os.path.basename(process) for process in processes]

    for model in models:
        llm = ProcessLLM(model, OPENAI_API_KEY)
        res_eval = []
        for process in processes:
            txt_process = open(f"../eval_code/data/{process}/{process}.txt", "r").read()
            try:
                res = llm.get_chain().invoke({"input": txt_process})

                if res == "There are some errors in the python code." or res == "Your process description does not contain any task.":
                    res_elem = [process, "", "", "", "", "", ""]
                else:
                    code = res["code"]
                    input_text = res["input"]
                    tools = res["tools"]
                    model = res["model"]
                    tasks = res["tasks"]
                    original_tasks = res["original_tasks"]

                    res_elem = [process, input_text, model, tasks, original_tasks, tools, code]
            except Exception as e:
                print(e)
                res_elem = [process, "", "", "", "", "", ""]
            res_eval.append(res_elem)
        
        res_df = pd.DataFrame(res_eval, columns=["process", "input", "model", "tasks", "tasks_original", "tools", "code"])

        res_df.to_csv('eval_code_gpt4.csv', sep=',', index=False)
