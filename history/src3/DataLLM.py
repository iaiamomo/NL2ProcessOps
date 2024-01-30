from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from CodeLLM import CodeLLM
from typing import List
import dotenv
import os
import json
import multiprocessing


TEMPLATE = """You are a very proficient assistant expert in Business Process Management tasks. You are able to extract the data flow from a python function enacting a natural language process description.

The output is a JSON string having the following format:
{{
    "dataFlow": [
        {{
            "name": <data_name>,
            "description": <data_description>,
            "type": <data_type>,
            "source": <source_name>
        }},
        ...
    ]
}}
The data flow is a comma-separated JSON list of data entities extracted from the python function enacting a process description. The python function is specified after the "Python function:" line. The process description is specified after "Process description:" line. 
Each data entity has a name, a type and a source. The source can be a task or an external entity (e.g., machine, human, system) or a data store (e.g., database, file). In case of a task, the source is the name of the tool performing that task, otherwise the source is the name of the external entity. The name of each data entity must be unique, do not add duplicates.

In order to generate the JSON data flow you have access to a set of tools able to perform part of the tasks of the process. The tools are specified after the "Tools:" line.
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

Generate the JSON data flow from the following python function and process description.
Python function: {code}
Process description: {input}
Answer:
"""

class CustomOutputParser(BaseOutputParser):
    """The output parser for the LLM."""
    def parse(self, text: str) -> str:
        out_txt = f"Data Flow:\n{text['dataFlow']}Python code:\n{text['code']}"
        return  out_txt

class DataLLM:

    def __init__(self, model, openai_key, temperature=0.0):
        self.cg_llm = CodeLLM(model, openai_key, temperature=temperature)

        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)

        self.prompt = ChatPromptTemplate.from_template(TEMPLATE)
        '''
        prompt takes as input:
            - tools: a list of tools
            - code: a python function
            - input: a process description
        '''

        self.output_parser = StrOutputParser()

        self.final_output_parser = CustomOutputParser()


    def get_chain(self):
        chain = self.prompt | self.model | self.output_parser
        return chain


    def parse_data_chain(self) -> Runnable:
        data_chain = self.get_chain()

        data_chain_output = {
            "dataFlow": data_chain,
            "inputs": RunnablePassthrough()
        }

        data_chain_output = data_chain_output | RunnableLambda(lambda x: {
            "dataFlow": x["dataFlow"],
            "code": x["inputs"]["code"],
            "input": x["inputs"]["input"]
        })

        return data_chain_output


    def parse_data_chain_output(self, data_chain_output: str) -> str:
        out_txt = f"Data Flow:\n{data_chain_output['dataFlow']}\nPython code:\n{data_chain_output['code']}"
        return out_txt

    def get_general_chain(self):
        cg_chain = self.cg_llm.get_general_chain()
        df_chain = self.parse_data_chain()

        chain = (
            cg_chain |
            df_chain |
            RunnableLambda(lambda x: self.parse_data_chain_output(x))
        )
        return chain


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo"
    llm = DataLLM(model, OPENAI_API_KEY)

    while True:
        input_text = input("Enter a process description: ")
        res = llm.get_general_chain().invoke({"input": input_text})
        print(res)

# The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.
        
# The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the identified markers are ok. If markers are not ok, the calibration process continues and another photo is capture. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.
