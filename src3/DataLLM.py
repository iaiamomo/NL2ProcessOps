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
            "actor": <source_name>
        }},
        ...
    ]
}}
The data flow is a comma-separated JSON list of data entities extracted from the python function enacting a process description. The python function is specified after the "Python function:" line. The process description is specified after "Process description:" line. 
Each data entity has a name, a type and a source. The source can be a task or an external entity (e.g., machine, human, system) or a data store (e.g., database, file). In case of a task, the source is the name of the actor performing that task, otherwise the source is the name of the external entity. The name of each data entity must be unique, do not add duplicates.

In order to generate the JSON data flow you have access to a set of tools able to perform part of the tasks of the process. The tools are specified after the "Tools:" line.
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
    - <actor_name> is the name of the actor performing the tool
Tools: {tools}

Generate the JSON data flow from the following python function and process description.
Python function: {code}
Process description: {input}
Answer:
"""

class DataLLM:

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_template(TEMPLATE)
        '''
        prompt takes as input:
            - tools: a list of tools
            - code: a python function
            - input: a process description
        '''
        self.output_parser = StrOutputParser()

    def get_chain(self):
        chain = self.prompt | self.model | self.output_parser
        return chain


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo"
    llm = DataLLM(model, OPENAI_API_KEY)

    user_r = ""
    while True:
        if user_r == "":
            user_r = input(f"Enter:\tp -> to enter a process description\n\tt -> to list tools\n\tat -> to add a tool\n\tq -> to quit\n")
        if user_r == "p":
            user_r = ""
            input_text = input("Enter a process description: ")
            res = llm.get_general_chain().invoke({"input": input_text})
            print(res)
            user_r = input(f"Enter:\te -> to simulate the process\n\tr -> to revise the process description\n\tq -> to quit\n")
            if user_r == "e":
                print("Executing...")
                try:
                    p = os.system("python process_code.py")
                    print(f"Process run with exit code {p}")
                except:
                    print("Error simulating the process")
                print("Done!")
            elif user_r == "r":
                print("Revising...")
                user_r = "p"
            elif user_r == "q":
                print("Quitting...")
                break
        elif user_r == "t":
            user_r = ""
        elif user_r == "at":
            user_r = ""
        elif user_r == "q":
            print("Quitting...")
            break

# The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.
        
# The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the identified markers are ok. If markers are not ok, the calibration process continues and another photo is capture. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.
