from langchain.schema.runnable import Runnable, RunnableLambda, RunnablePassthrough, RunnableBranch
from TasksModelLLM import MermaidLLM
from TasksPreProcessingLLM import TaskRetrieverLLM
from CodeLLM import CodeLLM
from ToolsManagerDB import ToolStore
import ast
import json
import os
import dotenv
from termcolor import colored
from langchain_openai import OpenAIEmbeddings


class ProcessLLM:

    def __init__(self, model="gpt-3.5-turbo", openai_key=None, temperature=0.0):
        self.model_tasks_llm = MermaidLLM(model, openai_key, temperature=temperature)
        self.task_llm = TaskRetrieverLLM(model, openai_key, temperature=temperature)
        self.code_llm = CodeLLM(model, openai_key, temperature=temperature)

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
                    #print(f"task: {task} tool: {elem['name']}")

        #print(f"Tools: {tool_list}")

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
        
        #print(f"Tasks: {result_list}")
        
        return True


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
            #print(e)
            error_python = True

        json_output = {
            "tools": output_chain["tools"],
            "code": output_chain["code"],
            "input": output_chain["input"],
            "model": output_chain["model"],
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
                "model": x["inputs"]["model"]
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
                "model": x["inputs"]["model"]
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

        # general chain that takes as input the process description, the model and the tools
        # it executes only if there are tasks in the process description
        general_chain = (
            RunnableLambda(lambda x: {
                "model": x["model"],
                "tools": self.tools_prompt_parser(x["tasks"]),
                "input": x["input"],
                })
            | code_llm_chain_output
            | RunnableBranch(
                (lambda x: not x["error_python"], RunnableLambda(lambda x: self.parse_output(x))),
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
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo-16k"
    model = "gpt-4-0125-preview"
    llm = ProcessLLM(model, OPENAI_API_KEY)

    while True:
        print(colored("Enter a process description: ", "green"))
        input_text = input()
        if input_text == "":
            continue
        res = llm.get_chain().invoke({"input": input_text})
        print(colored("Answer:\n", "green") + colored(res, "blue"))
        print(colored("Do you want to execute the process? (y)\nEnter a new process description? (p)\nQuit? (q)", "green"))
        user_r = input()
        if user_r == "y":
            print(colored("Executing...", "green"))
            try:
                print("Checking the sintax of the python file...")
                p = os.system("python -m py_compile llm_process_code.py")
                if p != 0:
                    print(colored("The python file has some sintax errors"), "red")
                else:
                    p = os.system("python llm_process_code.py")
                    print(colored(f"Process run with exit code {p}", "yellow"))
            except:
                print(colored("Error executin the process"), "red")
            print(colored("Execution done!", "green"))
            print(colored("Enter a new process description? (p)\nQuit? (q)", "green"))
            user_r = input()
        if user_r == "p":
            user_r = "p"
            continue
        else:
            print(colored("Quitting...", "green"))
            break
