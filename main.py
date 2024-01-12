import os
from dotenv import load_dotenv
from src.agent_memory import Agent

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

p_agent = Agent(OPENAI_KEY)

while True:
    input_text = input("Enter your query: ")
    p_agent.agent_runnable.invoke({"input": input_text}, config={"configurable": {"session_id": "foo"}})


# The process of calibration in a cardboard production consists of a continuous generation of a photo of the produced cardboard and anlysis of the number of threes present on it until the number of threes is less than 5. After this the process ends.
    
# Instead of ending the process, add an exclusive decision to check wheter the colors of the cardboard are ok or not. Then the process ends.
