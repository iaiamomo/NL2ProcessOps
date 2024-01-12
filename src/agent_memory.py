from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
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

system_prompt_3 = """
You are a very proficient assistant expert in Business Process Management tasks. You are able to extract the process model in Mermaid and generate the data flow diagram of the process based on the tools able to perform the task.

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

Finally you should execute the tools in the correct order and output the result of the execution.
"""


system_prompt_4 = """
You are a very proficient assistant expert in Business Process Management tasks. You are able to extract and adjust the process model in Mermaid, generate the data flow specification of the process based on the tools able to perform a particular task of the process, generate a pseudocode to enact the process and upon request simulate the process.

If the input is a description of the process, you should output the process model in Mermaid, the data flow represented as a list of tasks with the corresponding tools able to perform the tasks extracted from the process description. If none of the available tools fits the task, you should insert "null". Finally you should generate a pseudocode to enact the process.

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

If the input is a request to simulate the process, you should invoke the tools in the correct order and output the result of the execution based on the input and the output of the tools. If a tool is not available, simulate the result. Remember to perform the simulation based on the generated pseudocode.
"""

class Agent():

    def __init__(self, openai_key):
        # 1. define the model to use
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0.0)
        
        # 2. define the prompt to use
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_4),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # 3. define the tools to use
        self.tools = ToolRepo().get_tools()

        # 4. define agent
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)

        # 5. create the message history
        message_history = ChatMessageHistory()

        # 5. define agent executor
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

        # 6. define the runnable
        self.agent_runnable = RunnableWithMessageHistory(
            self.agent_executor,
            lambda session_id: message_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

