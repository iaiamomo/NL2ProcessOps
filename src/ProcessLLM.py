from langchain.schema.runnable import Runnable, RunnableLambda, RunnablePassthrough, RunnableParallel, RunnableBranch
from ModelTasksLLM import MermaidLLM
from TaskRetrieverLLM import TaskRetrieverLLM
from CodeLLM import CodeLLM
from DataLLM import DataLLM
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
        self.data_llm = DataLLM(model, openai_key, temperature=temperature)

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
            "error_python": error_python
        }
        
        return json_output


    def data_llm_parser(self) -> Runnable:
        data_llm_chain = self.data_llm.get_chain()

        data_llm_chain_output = {
            "dataFlow": data_llm_chain,
            "inputs": RunnablePassthrough()
        }

        data_llm_chain_output = (
            data_llm_chain_output 
            | RunnableLambda(lambda x: {
                "dataFlow": x["dataFlow"],
                "code": x["inputs"]["code"],
                "input": x["inputs"]["input"],
                "model": x["inputs"]["model"]
                })
        )

        return data_llm_chain_output


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
        out_txt = f"Data Flow:\n{output_chain['dataFlow']}\nPython code:\n{output_chain['code']}"
        return out_txt

    def get_chain(self):
        model_tasks_llm_chain_output = self.model_tasks_llm_parser()
        task_llm_chain_output = self.task_llm_parser()
        code_llm_chain_output = self.code_llm_parser()
        data_llm_chain_output = self.data_llm_parser()

        data_output_chain = (
            data_llm_chain_output
            | RunnableLambda(lambda x: self.parse_output(x))
        )

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
                (lambda x: not x["error_python"], data_output_chain),
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
        print(colored("Do you want to simulate the process? (s)\nEnter a new process description? (p)\nQuit? (q)", "green"))
        user_r = input()
        if user_r == "s":
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
                print(colored("Error simulating the process"), "red")
            print(colored("Simulation done!", "green"))
            print(colored("Enter a new process description? (p)\nQuit? (q)", "green"))
            user_r = input()
        if user_r == "p":
            user_r = "p"
            continue
        else:
            print(colored("Quitting...", "green"))
            break


"""
The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.

['capture photo of cardboard', 'analyze photo', 'set speed of die cutting machine to 10000 RPM']
['continuously capturing a photo of the cardboard being produced', 'analyzing each photo to check if all the markers identified are ok', 'setting the speed of the die cutting machine to 10000 RPM']

The manufacturing process of spindles in HSD company is fully automated. When a new order for a spindle arrives at the sales department, a new process instance is initiated. The warehouse system retrive the necessary raw materials, and in parallel the L12 line is set up for the assembly of the ordered spindle. Once the warehouse successfully retrieves the raw materials and the L12 lines is set up, the spindle is assembled over the L12 lines. Subsequently, the spindle undergoes testing and running-in in the smart tester. If the outcome of the test is negative, the spindle is sent to maintenance. Then, the process ends.

['new order for a spindle arrives', 'retrieval of raw materials', 'set up of L12 line', 'assembly of the spindle', 'testing and running-in of the spindle', 'maintenance of the spindle']
['a new order for a spindle arrives at the sales department', 'the warehouse system retrieves the necessary raw materials', 'the L12 line is set up for the assembly of the ordered spindle', 'the spindle is assembled over the L12 line', 'the spindle undergoes testing and running-in in the smart tester', 'if the outcome of the test is negative, the spindle is sent to maintenance', 'the process ends']
"""