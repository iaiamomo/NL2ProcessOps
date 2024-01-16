from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import StringPromptTemplate
from langchain.schema import BaseOutputParser
from utils.tools_chains import getTools
from typing import List
import os
import dotenv

TEMPLATE = """
You are a very proficient assistant expert in Business Process Management tasks. 

If the input is a description of a process you should output: 
    1. mermaid.js representing the process model following the BPMN 2.0 notation. Generate the mermaid.js within ```mermaid and ``` delimiters.
    2. generate the data flow specification of the process based on the tools able to perform a particular task of the process
        The data flow should have the following format:
        [
            {{
                "task": <task_name>,
                "tool": <tool_name>,
                "input_parameters": <input_parameters>,
                "output_parameters": <output_parameters>
            }},
            ...
        ]
        Generate the data flow specification within ```json and ``` delimiters.
    2. generate a python function that simulate the process. Include invocations of the identified tools able to perform the tasks extracted from the process description. Generate the python script within ```py and ``` delimiters.

If none of the available tools fits the task, you should insert "null". 

In order to generate the data flow and the python function, you have access to a set of tools, specified after the "Tools:" line.
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

Here's the process description and the tools available to you to generate the process model, the data flow and the python function.
Process Description: {input}
Tools: {tools}
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


class CustomOutputParser(BaseOutputParser):
    """The output parser for the LLM."""
    def parse(self, text: str) -> str:
        """Parse the output of an LLM call."""
        mermaid = False
        json = False
        python = False
        mermaid_text = ""
        json_text = ""
        python_text = ""
        for line in text.split("\n"):
            # check if the piece of text is a mermaid, json or python code
            if line.startswith("```mermaid"):
                mermaid = True
                json = False
                python = False
                continue
            elif line.startswith("```json"):
                mermaid = False
                json = True
                python = False
                continue
            elif line.startswith("```py"):
                mermaid = False
                json = False
                python = True
                continue
            elif line.startswith("```"):
                mermaid = False
                json = False
                python = False
            # add the line to the corresponding text
            if mermaid:
                mermaid_text += line + "\n"
            elif json:
                json_text += line + "\n"
            elif python:
                python_text += line + "\n"
        # if no mermaid, json or python code is found, return the original text
        if mermaid_text == "" and json_text == "" and python_text == "":
            return text
        # otherwise return the text with the mermaid, json and python code
        new_text = f"Mermaid proces model:\n{mermaid_text}\nData flow:\n{json_text}\nPython:\n{python_text}"
        return new_text


class ProcessAgent():
    """The agent designed for extracting the data flow and the process model from a process description."""

    def __init__(self, openai_key):
        """Initialize the agent."""

        # 1. load the model to use
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0.0)

        # 2. define the tools to use
        self.tools = getTools()

        # 3. define the prompt to use
        self.prompt = CustomPromptTemplate(
            template = TEMPLATE,
            tools = self.tools,
            input_variables=["input"]
        )

        # 4. define the output parser to use
        self.output_parser = CustomOutputParser()

    def get_chain(self):
        """Returns the chain of llm agent."""
        chain = self.prompt | self.llm | self.output_parser
        return chain


if __name__ == "__main__":
    # load the openai key
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # initialize the agent
    agent = ProcessAgent(OPENAI_API_KEY)
    # get the chain of the agent
    chain = agent.get_chain()
    # run the chain
    res = chain.invoke({"input": "The calibration process in a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check the number of markers. If the number of markers is greater then 4 the process ends."})
    print(res)
