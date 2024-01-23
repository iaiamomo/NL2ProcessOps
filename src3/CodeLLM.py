from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from langchain_openai import ChatOpenAI
from TaskRetrieverLLM import TaskRetrieverLLM
from ToolsManagerDB import ToolsManagerDB
import json
import dotenv
import os
import ast


TEMPLATE = """
You are a very proficient Python developer that generates a python function that implements a process description.

The process description is specified after the "Process description:" line. You should extract the start event, end event, tasks, exclusive gateways and parallel gateways from the process description and identify if there are loops and conditions. It is important that you identify the loops and the conditions. Then you should identify the tools able to perform the identified tasks. Finally you should generate the python function.

To generate the python code, you have access to a set of tools able to perform the tasks extracted from the process description. The tools are specified after the "Tools:" line.
Each tools is represented by a JSON string having the following structure:
{{
    "name": <class_name>,
    "description": <description>,
    "input_parameters": <input_parameters>,
    "output_values": <output_values>
}}
where:
    - <class_name> is the class of the tool
    - <description> is a string describing the tool
    - <input_parameters> is the list of input parameters of the tool, separated by a comma. Each input parameter has the following structure <name>:<type> where <name> is the name of the input parameter and <type> is the type of the input parameter. 
    - <output_values> is the list of output values of the tool
Tools: {tools}

The python function you have to generate, should use the tools provided whenever possible. To use them you need to use the .call() method with the proper input. Make sure to generate a correct and concise python function. You do not have to use all the tools available to you. It is important that you do not have to generate the python code for the identified tools, you can assume that the tools are already imported in the python function you have to generate, so no need to explicitly import them and define them. 
Generate the python function within the ```python and ``` markdown delimiters after the "Answer:" line. Always end the python function by a newline character and a triple backtick (```). It is important that after the return statement you add a newline character and a triple backtick (```). Do not add any other information after the triple backtick (```). The python function should be indented by 4 spaces.

Generate the python function from the following process description.
Process description: {input}
Answer:
"""


class CustomOutputParser(BaseOutputParser):
    """The output parser for the LLM."""
    def parse(self, text: str) -> str:
        # remove any newline character at the beginning and at the end of the string
        text = text.strip("\n")
        # remove any whitespace at the beginning and at the end of the string
        text = text.strip()
        # parse the output of the LLM
        """Parse the output of an LLM call."""
        # check that the string starts with a triple backtick followed by "py"
        # and ends with a triple backtick
        if not text.startswith("```python"):
            print(text)
            raise ValueError("The string should start with a triple backtick followed by python")
        if not text.endswith("```"):
            print(text)
            raise ValueError("The string should end with a triple backtick")
        # remove the triple backticks at the beginning and at the end and return the string
        # use the strip method to remove the triple backticks
        return text.strip("```python\n").strip("```")


class CodeLLM():

    def __init__(self, model, openai_key, temperature=0.0):
        self.tr_llm = TaskRetrieverLLM(model=model, openai_key=openai_key, temperature=temperature)

        self.tools_manager = ToolsManagerDB()

        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)

        self.prompt = ChatPromptTemplate.from_template(TEMPLATE)

        self.output_parser = CustomOutputParser()


    def is_list_of_tasks(self, task_retriever_output: str) -> bool:
        """Check if the output from the task retriever is a list of tasks"""
        # convert a string to list
        is_list = False
        tasks_list = self.serialize_tasks(task_retriever_output)
        if len(tasks_list) == 0:
            return is_list
        is_list = True
        return is_list
    

    def serialize_tasks(self, task_retriever_output: str) -> list:
        """Convert a string to a list"""
        try:
            result_list = ast.literal_eval(task_retriever_output)
            if not isinstance(result_list, list):
                return []
        except:
            result_list = []
        return result_list


    def parse_task_extractor_chain(self) -> Runnable:
        """Call the task retriever LLM to extract the list of tasks from the process description
        and construct a new output with the list of tasks and a flag indicating if the output is a list of tasks"""

        tr_chain = self.tr_llm.get_chain()

        task_extraction_chain_output = {
            "output": tr_chain,
            "process_description": RunnablePassthrough()
        }

        # check if the output is a list of tasks
        task_extraction_chain_output = task_extraction_chain_output | RunnableLambda(lambda x: {
            "has_tasks": self.is_list_of_tasks(x["output"]),
            "output": x["output"],
            "process_description": x["process_description"]})

        return task_extraction_chain_output


    def parse_tools_to_prompt(self, task_extraction_chain_output: dict) -> str:
        """Retrieve the list of tools from the tasks list"""
        if not task_extraction_chain_output["has_tasks"]:
            return ""

        tool_list = ""
        task_list = self.serialize_tasks(task_extraction_chain_output["output"])
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


    def get_chain(self):
        chain = self.prompt | self.model | self.output_parser
        return chain


    def parse_code_chain(self) -> Runnable:
        code_chain = self.get_chain()

        code_chain_output = {
            "code": code_chain,
            "inputs": RunnablePassthrough(),
        }

        code_chain_output = code_chain_output | RunnableLambda(lambda x: {
            "tools": x["inputs"]["tools"],
            "code": x["code"],
            "input": x["inputs"]["input"]
        })

        return code_chain_output


    def get_general_chain(self) -> str:
        # given a process description, extract the list of tasks
        task_extraction_chain_output = self.parse_task_extractor_chain()
        # given the list of tasks and the tools, extract the code
        code_chain_output = self.parse_code_chain()

        chain = (
            task_extraction_chain_output |
            RunnableLambda(lambda x: 
                {
                    "tools": self.parse_tools_to_prompt(x),
                    "input": x["process_description"]
                }) |
            code_chain_output
        )
        '''
        output of the chain:
            - tools: a list of tools
            - code: a python function
            - input: a process description
        '''

        return chain


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # gpt-4
    # gpt-3.5-turbo
    model = "gpt-3.5-turbo"
    llm = CodeLLM(model, OPENAI_API_KEY)
    chain_llm = llm.get_general_chain()

    while True:
        input_text = input("Enter the process description:\n")
        res = chain_llm.invoke({"input": input_text})
        print(f"Answer:{res}")


# The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.