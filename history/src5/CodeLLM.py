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


TEMPLATE = """You are a very proficient Python developer that generates a python function that implements a process description.

The process description is specified after the "Process description:" line. You should extract the start event, end event, tasks, exclusive gateways and parallel gateways from the process description and identify if there are loops and conditions. It is important that you identify the loops and the conditions. Then you should identify the tools able to perform the identified tasks. Finally you should generate the python function. To help you in generating the python code, you have access to the process model generated by the mermaid.js modeler. The mermaid.js process model is specified after the "Process model:" line.

To generate the python function, you have access to a set of tools able to perform the tasks extracted from the process description. The tools are specified after the "Tools:" line.
Each tools is represented by a JSON string having the following structure:
{{
    "name": <class_name>,
    "description": <description>,
    "input_parameters": <input_parameters>,
    "output_values": <output_values>,
    "actor": <actor_name>
}}
where:
    - <class_name> is the class of the tool
    - <description> is a string describing the tool
    - <input_parameters> is the list of input parameters of the tool, separated by a comma. Each input parameter has the following structure <name>:<type> where <name> is the name of the input parameter and <type> is the type of the input parameter. 
    - <output_values> is the list of output values of the tool
    - <actor_name> is the actor that can perform the task executed by the tool
Tools: {tools}

The python function you have to generate, should use the tools provided whenever possible. To use them you need to use the .call() static method with the proper input. Make sure to generate a correct and concise python function. You do not have to use all the tools available to you. You do not have to generate the python code for the identified tools, you can assume that the tools are already imported in the python function you have to generate, so no need to explicitly import them and define them. Add an invocation to the python function at the end of the python function you have to generate.
Generate the python function within the ```python and ``` markdown delimiters after the "Answer:" line. Always end the python function with an invocation to the generated function, you do not need to print the results. It is important that after the invocation statement you add a newline character and a triple backtick (```). Do not add any other information after the triple backtick (```). The python function should be indented by 4 spaces.

Generate the python function from the following process description.
Process description: {input}
Process model: {model}
Answer:
"""

TEMPLATE = """You are a very proficient Python developer that generates a python function that implements a process description.

The process description is specified after the "Process description:" line. You should extract the start event, end event, tasks, exclusive gateways and parallel gateways from the process description and identify if there are loops and conditions. It is important that you identify the loops and the conditions. Then you should identify the tools able to perform the identified tasks. Finally you should generate the python function. To help you in generating the python code, you have access to the process model generated by the mermaid.js modeler. The mermaid.js process model is specified after the "Process model:" line.

To generate the python function, you have access to a set of tools able to perform the tasks extracted from the process description. The tools are specified after the "Tools:" line.
Each tools is represented by a JSON string having the following structure:
{{
    "name": <class_name>,
    "description": <description>,
    "input_parameters": <input_parameters>,
    "output_values": <output_values>,
    "actor": <actor_name>
}}
where:
    - <class_name> is the class of the tool
    - <description> is a string describing the tool
    - <input_parameters> is the list of input parameters of the tool, separated by a comma. Each input parameter has the following structure <name>:<type> where <name> is the name of the input parameter and <type> is the type of the input parameter. 
    - <output_values> is the list of output values of the tool
    - <actor_name> is the actor that can perform the task executed by the tool
Tools: {tools}

The python function you have to generate, should use the tools provided whenever possible. To use them you need to use the .call() static method with the proper input. Make sure to generate a correct and concise python function. You do not have to use all the tools available to you. You do not have to generate the python code for the identified tools, you can assume that the tools are already imported in the python function you have to generate, so no need to explicitly import them and define them. Add an invocation to the python function at the end of the python function you have to generate.
Generate the python function within the ```python and ``` markdown delimiters after the "Answer:" line. Always end the python function with an invocation to the generated function, you do not need to print the results. It is important that after the invocation statement you add a newline character and a triple backtick (```). Do not add any other information after the triple backtick (```). The python function should be indented by 4 spaces.

Generate the python function from the following process description.
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

# The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.