from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from langchain_openai import ChatOpenAI


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

TEMPLATE = """Your task is to generates a Python code that implements a business process. The description of the business process is provided in the "Process description:" line.

To generate the Python code, you have access to the mermaid.js process model, which specifies the control flow of the process. Use it to help you generating a correct and concise Python code. The mermaid.js process model contains the start event, end event, tasks, exclusive gateways and parallel gateways, following the BPMN 2.0 notation. Based on these information decide whether to use if-else statements or parallel execution (threads) in the Python code. The mermaid.js process model is specified in the "Process model:" line.

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
The python code should use the tools to execute the process tasks whenever possible. To use the tools you need to use the .call() static method with the proper input (e.g., the tool with name BookAppointment which does not take inputs should be called with BookAppointment.call()).
You can assume that the classes implementing the tools are already already imported. You don't need to implement the classes of the tools. You only need to use them.
At the end of the Python code add the invocation of the function that implements the process. The invocation should be within the 'if __name__ == "__main__":' block.
Generate the python code within the ```python and ``` markdown delimiters after the "Answer:" line. Do not add any other information after the ```python and ``` markdown delimiters.

Process description: {input}
Process model: {model}
Answer:
"""

TEMPLATE = """\
You are given a process description and the process model depicting the control flow.

problem description:
=============
{input}
=============

process model:
======
{model}
======

Your goal is to generate a valid Python code that correctly implements the process description, using the following tools:
=============
{tools}
=============
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


Guidelines:
- Use the tools to execute the process tasks whenever possible. To use the tools you need to use the .call() static method with the proper input (e.g., the tool with name BookAppointment which does not take inputs should be called with BookAppointment.call()).
- Consider the tools already imported. You don't need to implement the classes of the tools. You only need to use them with the .call() method.
- Variables names you use should be meaningful.
- Double-check the generated code. It should generalize to any valid input, and not just the provided examples.
- Make sure to address the control flow provided by the process model. Use conditional statements (if-else) for exclusive gateways and parallel execution (threads) for parallel gateways.
- The code needs to be self-contained, and executable as-is.
- Do not add any other information after the ``` markdown end delimiters.

The generated code must follow this structure:
```python
def process(...):
    ...
    return ...

if __name__ == "__main__":
    ...
```

Answer:
```python
"""


class CustomOutputParser(BaseOutputParser):
    """The output parser for the LLM."""
    def parse(self, text: str) -> str:
        text = text.strip("\n")
        text = text.strip()
        # count how many ``` are in the text
        back_count = text.count("```")
        if back_count != 2:
            print(text)
            raise ValueError("The string should contain exactly two triple backticks")
        code = text.split("```")[1]
        code = code.strip().strip("python").strip()
        print(code)
        return code


class CodeLLM():

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_template(TEMPLATE)
        self.output_parser = CustomOutputParser()

    def get_chain(self):
        chain = self.prompt | self.model | self.output_parser
        return chain