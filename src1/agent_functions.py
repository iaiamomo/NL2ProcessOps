from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import StringPromptTemplate
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.schema import BaseOutputParser
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from utils.my_tools import ToolRepo
import dotenv
import os


TEMPLATE = """You are a very proficient assistant expert in Business Process Management tasks. You are able to extract and adjust the process model in mermaid.js, generate the data flow specification of the process based on the tools able to perform a particular task of the process, generate a pseudocode to enact the process and upon request simulate the process.

If the input is a description of the process, you should 
    1. output the process model in mermaid.js following the BPMN 2.0 notation, 
    2. output the data flow represented as a list of task with the corresponding tool able to perform the task extracted from the process description. If none of the available tools fits the task, you should insert "null". 
    3. generate a pseudocode to enact the process. You do not have to simulate the process by invoking the tools. Remember this.

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

If the input is a request to simulate the process, you should invoke the tools in the correct order following the pseudocode you generated. Please pass the input and the output of the tools to one another. If a tool is not available, output a random value. Remember to perform the simulation based on the generated pseudocode.
"""

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

class ProcessAgent():
    """The agent designed for extracting the data flow and the process model from a process description."""

    def __init__(self, openai_key):
        """Initialize the agent."""

        # 1. load the model to use
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0613", openai_api_key=openai_key, temperature=0.0)
        
        # 2. define the prompt to use
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", system_prompt_3,
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        
        # 3. define the tools to use
        self.tools = ToolRepo().get_tools()

        # 4. define the llm with tools
        self.llm_with_tools = self.llm.bind(functions=[format_tool_to_openai_function(t) for t in self.tools])

        # 6. define agent
        self.agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | self.prompt 
            | self.llm_with_tools 
            | OpenAIFunctionsAgentOutputParser()
        )

        # 7. define agent executor
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    p_agent = ProcessAgent(OPENAI_API_KEY)
    while True:
        input_text = input("Enter your request: ")
        p_agent = ProcessAgent(OPENAI_API_KEY)
        res = p_agent.agent_executor.invoke({"input": input_text})