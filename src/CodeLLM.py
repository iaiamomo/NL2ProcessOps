from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from langchain_openai import ChatOpenAI
import json
import dotenv
import os
import ast


TEMPLATE = """You are a helpful code assistant that generates a Python script that implements a business process. The description of the business process is provided in the "Process description:" line.

To generate the Python script, you have access to the mermaid.js process model, which specifies the control flow of the process. Use it to help you generating a correct and concise Python code. The mermaid.js process model contains the start event, end event, tasks, exclusive gateways and parallel gateways, following the BPMN 2.0 notation. The mermaid.js process model is specified in the "Process model:" line.

To generate the Python code, you have access to a set of function able to perform the tasks of the process. The functions are specified after the "Functions:" line. 
You can assume that the functions are already imported in the python script you have to generate, so no need to explicitly import or define them.
Each function is represented by a JSON string having the following structure:
{{
    "name": <class_name>,
    "description": <description>,
    "input_parameters": <input_parameters>,
    "output_values": <output_values>,
    "actor": <actor_name>
}}
where:
    - <class_name> is the class of the function
    - <description> is a string describing what the function does
    - <input_parameters> is the list of input parameters of the tool, separated by a comma. Each input parameter has the following structure <name>:<type> where <name> is the name of the input parameter and <type> is the type of the input parameter. 
    - <output_values> is the list of output values of the tool, separated by a comma. Each output value has the following structure <name>:<type> where <name> is the name of the output value and <type> is the type of the output value.
    - <actor_name> is the actor that can perform the task executed by the function
Functions: {tools}

The python code should use the functions to simulate the process whenever possible. To use them you need to use the .call() static method with the proper input. Remember you don't have to explicitly define the functions.
Generate the python function within the ```python and ``` markdown delimiters after the "Answer:" line. 

Process description: {input}
Process model: {model}
Answer:
"""

# The exclusive gateways are represented by {{x}} and represent an condition (e.g., if-else). The parallel gateways are represented by {{AND}} and represent a parallel execution (e.g., threads).
TEMPLATE = """You are a helpful code assistant that generates a Python code that implements a business process. The description of the business process is provided in the "Process description:" line.

To generate the Python code, you have access to the mermaid.js process model, which specifies the control flow of the process. Use it to help you generating a correct and concise Python code. The mermaid.js process model contains the start event, end event, tasks, exclusive gateways and parallel gateways, following the BPMN 2.0 notation. The mermaid.js process model is specified in the "Process model:" line.

To generate the Python code, you have access to a set of tools able to perform the tasks of the process. The tools are specified after the "Tools:" line. 
Each tool is represented by a JSON string having the following structure:
{{
    "name": <class_name>,
    "description": <description>,
    "input_parameters": <input_parameters>,
    "output_values": <output_values>,
    "actor": <actor_name>
}}
where:
    - <class_name> is the class implementing the tool.
    - <description> is a string describing what the tool is able to do.
    - <input_parameters> is the list of input parameters of the tool, separated by a comma. Each input parameter has the following structure <name>:<type> where <name> is the name of the input parameter and <type> is the type of the input parameter.
    - <output_values> is the list of output values of the tool, separated by a comma. Each output value has the following structure <name>:<type> where <name> is the name of the output value and <type> is the type of the output value.
    - <actor_name> is the actor that can perform the task executed by the tool.
Tools: {tools}

Generate the python code in the 'def process():' function and add the invocation of the function in the 'if __name__ == "__main__":' block.
The python code should use the tools to execute the process tasks whenever possible. To use the tools you need to use the .call() static method with the proper input (e.g., the tool with name BookAppointment which does not take inputs should be called with BookAppointment.call()). You can assume that the classes implementing the tools are already already imported. You don't need to implement the classes of the tools. You only need to use them.
At the end of the Python code add the invocation of the function that implements the process. The invocation should be within the 'if __name__ == "__main__":' block.
Generate the python code within the ```python and ``` markdown delimiters after the "Answer:" line.

Process description: {input}
Process model: {model}
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
        print(text)
        return text.strip("```python").strip().strip("```").strip()


class CodeLLM():

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_template(TEMPLATE)
        self.output_parser = CustomOutputParser()

    def get_chain(self):
        chain = self.prompt | self.model | self.output_parser
        return chain
