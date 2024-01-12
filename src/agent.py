from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from src.tools import ToolRepo

'''
prompt structure
1. general description of what he is able to do
2. description of the output
3. examples of the output
3. input
'''

system_prompt_1 = """
You are a very proficient assistant expert in Business Process Management tasks. You are able to extract the process model in Mermaid and generate the data flow diagram of the process.

You should output a list of JSON string representing the data flow and the process model depicted in Mermaid.

The data flow should have the following format:
[
    {{
        "tool": <tool_name>,
        "input_parameters": <input_parameters>,
        "output_parameters": <output_parameters>
    }},
    ...
]
"""


system_prompt_4 = """
You are a very proficient assistant expert in Business Process Management tasks. You are able to extract the process model in Mermaid and generate the data flow specification of the process based on the tools able to perform a particular task in the process.

You should output the process model in Mermaid and the data flow represented as a list of tasks with the corresponding tools able to perform the tasks extracted from the process description.

The data flow should have the following format:
[
    {{
        "tool": <tool_name>,
        "input_parameters": <input_parameters>,
        "output_parameters": <output_parameters>
    }},
    ...
]

If none of the tools fits the task, you should insert "null". Do not add any other information.

Finally you should generate a python script that executes the tools in the correct order and output the result of the execution.
"""


system_prompt_2 = """
You are a very proficient assistant expert in Business Process Management and particularly good at extracting the process model and the data flow from a process description. The data flow represents the movement of information between different activities and focuses on how data is input, processed and output. The control flow governs the sequence and conditions under which activities are executed and defines the logical order of tasks and decision points. 

The input may be a description of the process. If this is the case, you should output a list of JSON string representing the data flow of the process and having the following format:
[
    {{
        "call": <function_call>,
        "input_parameters": <input_parameters_description>,
        "output_parameters": <output_parameters_description>
    }},
    ...
]
Additionally, you should output a Mermaid diagram representing the process model.

The JSON data flow is a list of input and output parameters. For instance if the input is "The process starts with the user filling in the form and then the form is sent to the manager for approval", the output should be:
[
    {{
        "call": "fill_form",
        "input_parameters": "user",
        "output_parameters": "form"
    }},
    {{
        "call": "send_form",
        "input_parameters": "form",
        "output_parameters": ""
    }}
]
The mermaid diagram should be a string representing the process model in Mermaid. For instance, if the input is "The process starts with the user filling in the form and then the form is sent to the manager for approval", the output should be:
graph TD
    user --> form
    form --> manager

If none of the tools fit the description, you should output "null". Do not add any information.

Provide the JSON data flow and the mermaid process model for the following description after the prompt "Description". Please follow the format described above for the JSON data flow and mermaid process model. 
"""

class Agent():

    def __init__(self, openai_key):
        # 1. define the model to use
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0.0)
        
        # 2. define the prompt to use
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_4),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        # 3. define the tools to use
        self.tools = ToolRepo().get_tools()

        # 4. define agent
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)

        # 5. define agent executor
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
