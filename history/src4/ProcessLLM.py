from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough, RunnableParallel
from ModelLLM import MermaidLLM
from TaskRetrieverLLM import TaskRetrieverLLM
from CodeLLM import CodeLLM
from DataLLM import DataLLM
from ToolsManagerDB import ToolsManagerDB
import ast
import json
import os
import dotenv
from termcolor import colored

class ProcessLLM:

    def __init__(self, model="gpt-3.5-turbo", openai_key=None, temperature=0.0):
        self.model_llm = MermaidLLM(model, openai_key, temperature=temperature)
        self.task_llm = TaskRetrieverLLM(model, openai_key, temperature=temperature)
        self.code_llm = CodeLLM(model, openai_key, temperature=temperature)
        self.data_llm = DataLLM(model, openai_key, temperature=temperature)
        self.tools_manager = ToolsManagerDB(openai_key)


    def tools_prompt_parser(self, task_llm_output: dict) -> str:
        """Retrieve the list of tools from the tasks list"""
        if not task_llm_output["has_tasks"]:
            return ""

        tool_list = ""
        task_list = ast.literal_eval(task_llm_output["output"])
        for task in task_list:
            # retrieve the tool
            res = self.tools_manager.tool_store.search(task)
            tool_desc = {
                "name": res["output"]["name"],
                "description": res["output"]["description"],
                "input_parameters": res["output"]["input_parameters"],
                "output_parameters": res["output"]["output_parameters"]
            }
            tool_desc_str = json.dumps(tool_desc)
            if tool_desc_str not in tool_list:
                tool_list += f"{json.dumps(tool_desc)}\n"

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
        return True


    def save_code(self, output_chain) -> Runnable:
        tools = output_chain["tools"]
        tools_list = tools.split("}}}\n")

        py_file = ""
        
        # import all the used tools
        for elem in range(len(tools_list)-1):
            tool_str = tools_list[elem] + "}}}"
            tool = json.loads(tool_str)
            class_name = tool["name"]
            py_file += f"from tools.{class_name} import {class_name}\n"
        
        # add the python function
        py_file += "\n"
        py_file += output_chain["code"]

        function_name = ""
        tree = ast.parse(py_file)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name

        lines_py_file = py_file.strip("\n").split("\n")
        if function_name not in lines_py_file[-1]:
            py_file += f"\n\nif __name__ == '__main__':\n\t{function_name}()"

        with open("process_code.py", "w+") as f:
            f.write(py_file)
        
        json_output = {
            "tools": output_chain["tools"],
            "code": output_chain["code"],
            "input": output_chain["input"],
            "model": output_chain["model"]
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
            "output": task_llm_chain,
            "input": RunnablePassthrough()
        }

        # check if the output is a list of tasks
        task_llm_chain_output = (
            task_llm_chain_output 
            | RunnableLambda(lambda x: {
                "has_tasks": self.is_list_of_tasks(x["output"]),
                "output": x["output"],
                "input": x["input"]
                })
        )

        return task_llm_chain_output


    def model_llm_parser(self) -> Runnable:
        model_llm_chain = self.model_llm.get_chain()

        model_llm_chain_output = {
            "model": model_llm_chain,
            "inputs": RunnablePassthrough()
        }

        model_llm_chain_output = (
            model_llm_chain_output
            | RunnableLambda(lambda x: {
                "model": x["model"],
                "input": x["inputs"]["input"]
                })
        )

        return model_llm_chain_output


    def parse_output(self, output_chain: dict) -> str:
        out_txt = f"Data Flow:\n{output_chain['dataFlow']}\nPython code:\n{output_chain['code']}"
        return out_txt

    def get_chain(self):
        model_llm_chain_output = self.model_llm_parser()
        task_llm_chain_output = self.task_llm_parser()
        code_llm_chain_output = self.code_llm_parser()
        data_llm_chain_output = self.data_llm_parser()

        chain = (
            RunnableParallel({
                "model": model_llm_chain_output,
                "tasks": task_llm_chain_output
                })
            | RunnableLambda(lambda x: {
                "model": x["model"]["model"],
                "tools": self.tools_prompt_parser(x["tasks"]),
                "input": x["model"]["input"],
                })
            | code_llm_chain_output
            | data_llm_chain_output
            | RunnableLambda(lambda x: self.parse_output(x))
        )

        return chain


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo"
    llm = ProcessLLM(model, OPENAI_API_KEY)

    while True:
        print(colored("Enter a process description: ", "green"))
        input_text = input()
        res = llm.get_chain().invoke({"input": input_text})
        print(colored("Answer:\n", "green") + colored(res, "blue"))
        print(colored("Do you want to simulate the process? (s)\nRevise the output? (r)\nQuit? (q)", "green"))
        user_r = input()
        if user_r == "s":
            while True:
                print(colored("Executing...", "green"))
                try:
                    p = os.system("python process_code.py")
                    print(colored(f"Process run with exit code {p}", "yellow"))
                except:
                    print(colored("Error simulating the process"), "red")
                print(colored("Simulate again? (s)\nRevise the output? (r)\nQuit? (q)", "green"))
                input_s = input()
                if input_s == "r" or input_s == "q":
                    user_r = input_s
                    break
            print(colored("Simulation done!", "green"))
        if user_r == "r":
            print(colored("Revising...", "green"))
            user_r = "p"
            continue
        if user_r == "q":
            print(colored("Quitting...", "green"))
            break

    '''while True:
        print("Enter a process description: ")
        input_text = input()
        res = llm.get_chain().invoke({"input": input_text})
        print("Answer:\n" + res)
        print("Do you want to simulate the process? (s)\nRevise the output? (r)\nQuit? (q)")
        user_r = input()
        if user_r == "s":
            while True:
                print("Executing...")
                try:
                    p = os.system("python process_code.py")
                    print(f"Process run with exit code {p}")
                except:
                    print("Error simulating the process")
                print("Simulate again? (s)\nRevise the output? (r)\nQuit? (q)")
                input_s = input()
                if input_s == "r" or input_s == "q":
                    user_r = input_s
                    break
            print("Simulation done!")
        if user_r == "r":
            print("Revising...")
            continue
        if user_r == "q":
            print("Quitting...")
            break'''

# The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.
