from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import importlib.util
import os
import dotenv
import random

TEMPLATE = """Provide me a description for a given python function that execute a particular task in the manufacturing domain.

You are given as input the python function, its name and the actor executing the task after the Python function: line.

You have to generate a description having the following format:
description = {{
    "description": <string representing the description of the task is going to be executed>,
    "more details": <string representing what are the input and output parameters of the task, if they exist>,
    "input_parameters": <list of strings representing the input parameters of the task, e.g., ["part_list:list"]>,
    "output_parameters": <list of string representing the output parameters of the task, e.g., ["retrieved:bool"]>,
    "actor": <actor name>
}}

Here are a few examples:
1. Python function:
    {{
        "function": "
            def call(part_list : list) -> bool:
                retrieved = True
                return retrieved
        ",
        "name": "RetrievePart",
        "actor": "wms_is"
    }}
   Description:
    description = {{
        "description": "Retrieve raw materials",
        "more details": "This tool takes as input the part list of a product. It returns a boolean indicating if all the parts are retrieved.",
        "input_parameters": ["part_list:list"],
        "output_parameters": ["retrieved:bool"],
        "actor": "wms_is"
    }}

2. Python function:
    {{
        "function": "
            def call(product_id : int) -> bool:
                passed = True
                return passed
        ",
        "name": "TestProduct",
        "actor": "smart_tester"
    }}
   Description:
   description = {{
        "description": "Test and run-in of the product",
        "more details": "It takes as input the identificator of the product to be tested. It returns a boolean value, True if the product passed the test, False otherwise.",
        "input_parameters": ['product_id:int'],
        "output_parameters": ['passed:bool'],
        "actor": "smart_tester"
    }}

3. Python function:
    {{
        "function": "
            def call(image: np.matrix) -> bool:
                markers_ok = True
                return markers_ok
        ",
        "name": "CheckMarkers",
        "actor": "vision_is"
    }}
   Description:
    description = {{
        "description": "Analysis of the markers on an image",
        "more details": "This tool takes as input an image. It returns a boolean indicating if markers are present.",
        "input_parameters": ["image:np.matrix"],
        "output_parameters": ["markers_ok:bool"],
        "actor": "vision_is"
    }}

Python function: {python_function}
Description:
"""


class ToolDocLLM:

    def __init__(self, model="gpt-3.5-turbo", openai_key=None, temperature=0.0):
        #model = "gpt-4"
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = PromptTemplate.from_template(TEMPLATE)
        self.output_parser = StrOutputParser()

    def get_chain(self):
        return self.prompt | self.model | self.output_parser


def generate_process_description():
    dotenv.load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    toolDoc = ToolDocLLM(openai_key=openai_key)

    python_function = """{
        "function": "
            def call(product_id : int) -> bool:
                cooked = True
                return cooked
        ",
        "name": "Cook",
        "actor": "oven"
    }"""

    res = toolDoc.get_chain().invoke({"python_function": python_function})
    print(res)


if __name__ == '__main__':
    generate_process_description()
