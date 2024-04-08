from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from langchain_openai import ChatOpenAI


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
- in case of invocation of threads, if the threds are executed in parallel, you need to add the invocation parallel() before the thread definition and execution, and end_parallel() after the thread execution.
- in case of if statements, you need to put the condition inside the check() function. e.g., if "if a > b:" is called, you need to replace it with "check(a > b):".
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
        #print(code)
        return code


class CodeLLM():

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_template(TEMPLATE)
        '''
        prompt takes as input:
            - tools: a list of tools
            - model: model of the process
            - input: a process description
        '''
        self.output_parser = CustomOutputParser()

    def get_chain(self):
        chain = self.prompt | self.model | self.output_parser
        return chain