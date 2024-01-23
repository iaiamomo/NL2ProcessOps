from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from utils.my_tools import ToolRepo
from utils.tools_chains import getTools
import dotenv
import os


TEMPLATE_1 = """You are a very proficient assistant expert in Business Process Management tasks. You are able to extract and adjust the process model in Mermaid, generate the data flow specification of the process based on the tools able to perform a particular task of the process, generate a pseudocode to enact the process and upon request simulate the process.

If the input is a description of the process, you should output the process model in Mermaid, the data flow represented as a list of tasks with the corresponding tools able to perform the tasks extracted from the process description. If none of the available tools fits the task, you should insert "null". Finally you should generate a python code to enact the process. You do not have to simulate the process by invoking the tools.

The data flow should have the following format:
[
    {{
        "task": <task_name>,
        "tool": <tool_name_if_available>,
        "input_parameters": <input_parameters>,
        "output_parameters": <output_parameters>
    }},
    ...
]
"""

TEMPLATE_3 = """You are very proficient in taking a natural language description of a process and generating the data flow.

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

The data flow is a comma-separated JSON list of tasks and data entities extracted from the process description. Each task has a name, a description, a tool, a list of input data and a list of output data. If the task does not have input or output data, the corresponding list is empty. A task can have only one tool. If none of the available tools fits a task, you should insert "null". Each data entity has a name, a type and a source. The source can be a task or an external entity (e.g., machine, human, system) or a data store (e.g., database, file). In case of a task, the source is the name of the tool performing that task, otherwise the source is the name of the external entity.

Output the data flow within ```json and ``` delimiters

Generate the JSON data flow from the following process description. You should generate the JSON data flow of the process description using only the tools able to perform tasks described in the process description. You do not have to use all the tools available to you.
Process description: {input}
"""

class CustomAgent():

    def __init__(self, openai_key):
        # 1. define the model to use
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0.0)

        # 2. define the prompt to use
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", TEMPLATE_3),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        # 3. define the tools to use
        self.tools = getTools()

        # 4. define agent
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)

        # 5. define agent executor
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    p_agent = CustomAgent(OPENAI_API_KEY)
    while True:
        input_text = input("Enter the process description: ")
        p_agent.agent_executor.invoke({"input": input_text})