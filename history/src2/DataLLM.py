from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import StringPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.tools_chains import getTools
from typing import List
import dotenv
import os

TEMPLATE = """You are a very proficient assistant expert in Business Process Management tasks. You are able to extract the data flow from a from a process description. To do so, first you should extract the start event, end event, task, exclusive gateway and parallel gateway from the process description. Then you should identify the tools able to perform the tasks. Finally you should generate the data flow represented as a list of tasks with the corresponding tools able to perform the tasks extracted from the process description. If none of the available tools fits the task, you should insert "null".
The data flow should have the following format:
[
    {{
        "task": <task_name>,
        "description": <task_description>,
        "tool": <tool_name>,
        "input": [
            {{
                "name": <input_name>,
                "type": <input_type>,
            }},
            ...
        ]
        "output_parameters": [
            {{
                "name": <output_name>,
                "type": <output_type>
            }},
            ...
        ]
    }},
    ...
]

Include the JSON data flow inside markdown code block:
```json
```
Do not add any other text. Only json code block.

This is the list of available tools:
{tools}

Generate the data flow for the following process description: {input}
"""

TEMPLATE_2 = """You are a very proficient assistant expert in Business Process Management tasks. You are able to extract the mermaid.js data flow diagram from a from a process description. 

To generate the mermaid.js data flow, you should 
    extract the start event, end event, tasks, exclusive gateways and parallel gateways from the process description.
    from the available tools select those able to perform the extracted tasks. If none of the available tools fits a task, you should insert "null".
    from the descriptions of the identified tools and the process description identify if external entities (e.g., machines, people, systems) are involved.
    from the descriptions of the identified tools and the process description identify if data stores (e.g., databases, files) are involved.
    from the descriptions of the identified tools and the process description identify the data flow among tasks, data stores and external entities.

The mermaid js data flow should have the following format:
The graph must use the TD (Top to Down) direction.
Each mermaid js node must have the following structure:
    id:type:shape and text
        id - it is a unique identifier. Integer from 1 to n. Each node has a unique identifier
        type - defines the type of the element. Possible types are: tasks, data stores and external entities.
        Based on the type of the node following shapes and texts are to be used:
            task: ((tool name))     i.e., id:task:((tool name))
            datastore: (datastore label)     i.e., id:datastore:(datastore label)
            externalentity: [externalentity label]     i.e., id:externalentity:[externalentity label]
    All nodes that have occurred more than once should have following structure: id:type: (i.e., 2:task:) by futher occurrence. It is strictly prohibited to use only id (i.e. 2) as a reference.
If there is a data flow between two tasks, data stores and external entities it is necessary to use the direction.
    direction: -->

This is the list of available tools:
{tools}

Generate the mermaid.js data flow of the following process description: {input}
"""

TEMPLATE_3 = """You are very proficient in taking a natural language description of a process and extracting the data flow.

The output is a JSON string having the following format:
{{
    "tasks": [
        {{
            "name": <task_name>,
            "description": <task_description>,
            "tool": <tool_name>,
            "input": ["input_data_name", ...],
            "output": ["output_data_name", ...]
        }},
        ...
    ].
    "dataEntities": [
        {{
            "name": <data_name>,
            "type": <data_type>,
            "source": <source_name>
        }},
        ...
    ]
}}

The data flow is a comma-separated JSON list of tasks and data entities extracted from the process description. The process description is specified after "Process description:" line. Each task has a name, a description, a tool, a list of input data and a list of output data. If the task does not have input or output data, the corresponding list is empty. A task can have only one tool. If none of the available tools fits a task, you should insert "null". Each data entity has a name, a type and a source. The source can be a task or an external entity. In case of a task, the source is the name of the tool performing that task, otherwise the source is the name of the external entity.

In order to generate the JSON data flow of the process description you have access to a set of tools able to perform part of the tasks extracted from the process description.
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

Here's the process description and the tools available to you to extract the data flow from the process description. You should generate the JSON data flow of the process description using only the tools able to perform tasks described in the process description. You do not have to use all the tools available to you.
Process description: {input}
Tools: {tools}
Answer:
"""


TEMPLATE_4 = """You are very proficient in taking a natural language description of a process and generating the data flow.

The output is a JSON string having the following format:
{{
    "tasks": [
        {{
            "name": <task_name>,
            "description": <task_description>,
            "tool": <tool_name>,
            "input": [<input_data_name>, ...],
            "output": [<output_data_name>, ...]
        }},
        ...
    ].
    "dataEntities": [
        {{
            "name": <data_name>,
            "description": <data_description>,
            "type": <data_type>,
            "source": <source_name>
        }},
        ...
    ]
}}

The data flow is a comma-separated JSON list of tasks and data entities extracted from the process description. The process description is specified after "Process description:" line. Each task has a name, a description, a tool, a list of input data and a list of output data. If the task does not have input or output data, the corresponding list is empty. A task can have only one tool. If none of the available tools fits a task, you should insert "null". Each data entity has a name, a type and a source. The source can be a task or an external entity (e.g., machine, human, system) or a data store (e.g., database, file). In case of a task, the source is the name of the tool performing that task, otherwise the source is the name of the external entity.

In order to generate the JSON data flow of the process description you have access to a set of tools able to perform part of the tasks extracted from the process description.
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

Generate the JSON data flow from the following process description. You should generate the JSON data flow of the process description using only the tools able to perform tasks described in the process description. You do not have to use all the tools available to you.
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

class DataLLM:

    def __init__(self, openai_key):
        self.model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0.0)

        self.tools = getTools()

        self.prompt = CustomPromptTemplate(
            template = TEMPLATE_4,
            tools = self.tools,
            input_variables=["input"]
        )

        self.output_parser = StrOutputParser()

        self.chain = self.prompt | self.model | self.output_parser

if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm = DataLLM(OPENAI_API_KEY)

    while True:
        input_text = input("Enter the process description: ")
        res = llm.chain.invoke({"input": input_text})
        print(res)
    
    p1 = "The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends."

    res = llm.chain.invoke({"input": p1})
    print(res)