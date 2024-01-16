from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import StringPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.tools_chains import getTools
from typing import List
import dotenv
import os

TEMPLATE_4 = """You are very proficient python developer that generates a python function based on a process description.

The process description is a natural language description of a process. In order to generate the python function you should extract the tasks, flow, loops and conditions from the process description. The tasks extracted from the process description should be represented by a python function. The loops extracted from the process description should be represented by a while loop. The conditions extracted from the process description should be represented by an if statement.

To generate the python code you have access to a set of tools able to perform part of the tasks extracted from the process description.
You can assume that the tools are already imported in the python script you have to generate, so no need to explicitly import or define them.
Each tool is a python function that is represented by a JSON string having the following structure:
{{
    "name": <name>,
    "description": <description>,
    "input_parameters": <input_parameters>,
    "output_values": <output_values>
}}
where:
    - <name> is the name of the tool
    - <description> is a string describing the tool
    - <input_parameters> is the list of input parameters of the tool, separated by a comma. Each input parameter has the following structure <name>:<type> where <name> is the name of the input parameter and <type> is the type of the input parameter. 
    - <output_values> is the list of output values of the tool
Here is the list of available tools: {tools}

The python function should use the tools provided whenever possible.
Make sure to generate a correct and concise python function. Output the python code within ```python and ``` delimiters.

Generate the python function from the following process description. To do so, you should extract the tasks, loop and conditions from the process description. Then you shoul identify the tools able to perform the identified tasks. Finally you should generate the python function. Remember that you do not have to generate the python code for the tools, you can assume that the tools are already imported in the python script you have to generate, so no need to explicitly import them and define them. You do not have to use all the tools available to you.
Process description: {input}
Answer:
"""

TEMPLATE_5 = """You are a very proficient Python developer that generates a python function that implements a process description.

The process description is specified after the "Process description:" line. You should extract the start event, end event, tasks, exclusive gateways and parallel gateways from the process description and identify if there are loops and conditions in the process description. Then you should identify the tools able to perform the identified tasks. Finally you should generate the python function.

To generate the python code, you have access to a set of tools able to perform the tasks extracted from the process description. The tools are specified after the "Tools:" line.
Each tools is represented by a JSON string having the following structure:
{{
    "name": <name>,
    "description": <description>,
    "input_parameters": <input_parameters>,
    "output_values": <output_values>
}}
where:
    - <name> is the name of the tool
    - <description> is a string describing the tool
    - <input_parameters> is the list of input parameters of the tool, separated by a comma. Each input parameter has the following structure <name>:<type> where <name> is the name of the input parameter and <type> is the type of the input parameter. 
    - <output_values> is the list of output values of the tool
Tools: {tools}

The python function you have to generate, should use the tools provided whenever possible. Make sure to generate a correct and concise python function. You do not have to use all the tools available to you. It is important that you do not have to generate the python code for the identified tools, you can assume that the tools are already imported in the python function you have to generate, so no need to explicitly import them and define them. Output only the python function you have generated from the process description within ```python and ``` markdown delimiters.

Generate the python function from the following process description.
Process description: {input}
Answer:
"""

class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[BaseTool]
    
    def generate_tools_documentation(self) -> str:
        """Generate the documentation for the tools."""
        # Get the list of strings containing the documentation for each tool
        tool_name_to_documentation = []
        for tool in self.tools:
            # get the description of the tool 
            tool_description = tool.description
            # add the documentation for the tool to the list
            tool_name_to_documentation.append(tool_description)
        # return the string containing the documentation for the tools
        return "\n".join(tool_name_to_documentation)

    def format(self, **kwargs) -> str:
        # add the tool documentation to the kwargs
        kwargs["tools"] = self.generate_tools_documentation()
        return self.template.format(**kwargs)

class CodeLLM:

    def __init__(self, openai_key):
        self.model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0.0)

        self.tools = getTools()

        self.prompt = CustomPromptTemplate(
            template = TEMPLATE_5,
            tools = self.tools,
            input_variables=["input"]
        )

        self.output_parser = StrOutputParser()

        self.chain = self.prompt | self.model | self.output_parser

if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm = CodeLLM(OPENAI_API_KEY)

    while True:
        input_text = input("Enter the process description: ")
        res = llm.chain.invoke({"input": input_text})
        print(res)
    
    p1 = "The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends."

    res = llm.chain.invoke({"input": p1})
    print(res)