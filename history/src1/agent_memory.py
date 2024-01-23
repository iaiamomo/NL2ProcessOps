from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils.my_tools import ToolRepo
from utils.tools_chains import getTools
import dotenv
import os

system_prompt_3 = """
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

If the input is a request to simulate the process, you should invoke the tools in the correct order and output the result of the execution based on the input and the output of the tools. Remember to perform the invocation based on the generated pseudocode.
"""


class AgentMemory():

    def __init__(self, openai_key):
        # 1. define the model to use
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0.0)
        
        # 2. define the prompt to use
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_3),
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


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    p_agent = AgentMemory(OPENAI_API_KEY)
    while True:
        input_text = input("Enter your request: ")
        p_agent.agent_runnable.invoke({"input": input_text}, config={"configurable": {"session_id": "foo"}})


# The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.

# The process of calibration in a cardboard production consists of a continuous capturing of a photo of the produced cardboard until the number of markers is greater than 4. After this the process ends.

# The calibration process in a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check the number of markers. If the number of markers is greater then 4 the process ends.

# Instead of ending the process, if the number of markers is greater than 4, set the speed of the die cutting machine to 10000 RPM. Then end the process.
