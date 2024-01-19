from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import dotenv
import os

# few-shot prompting

TEMPLATE = """You are a very proficient assistant expert in Business Process Management tasks. You are able in taking a natural language process description and extracting the underline start event, end event, task, exclusive gateway and parallel gateway from the process description. Your goal is to output a list of the extracted tasks.

The output is a list of strings. Each string contains a high level description of a task.

If the process description does not contains any task, the output is an empty list.

Here are a few examples of process descriptions and the expected output:

1. Process description: When a pallet arrives at the working station, the system empties the scan results. Then the worker scans the order. Afterwards the system displays the scanning UI to the worker and in parallel, the worker assembles the part.
   Response: ["empty the scan results", "scan the order", "display the scanning UI", "assemble the part"]

2. Process description: The warehouse of Grimaldi is a warehouse that stores cardboard rolls. A cardboard roll is used to produce cardboards. There exists two types of cardboard: the white cardboard and the brown cardboard. The warehouse stores the cardboard rolls depending on the type of cardboard. When a new cardboard roll arrives at the warehouse, the worker checks the type of cardboard and enter this information inside the WMS system. The system automatically capture an image of the current status of the warehouse. By analyzing the image, the system identifies the location where the cardboard roll should be stored. Then the worker stores the cardboard rool in the warehouse and the system updates the quantity of that cardboard rolls in the warehouse.
   Response: ["check the type of cardboard", "enter the information inside the WMS system", "capture an image of the current status of the warehouse", "identify the location where the cardboard roll should be stored", "store the cardboard rool in the warehouse", "update the quantity of that cardboard rolls in the warehouse"]

Process description: {input}
Response:
"""

class TaskRetrieverLLM():

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)

        self.prompt = PromptTemplate.from_template(TEMPLATE)

        self.output_parser = StrOutputParser()

    def get_chain(self) -> str:
        chain = self.prompt | self.model | self.output_parser
        return chain



if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm = TaskRetrieverLLM(OPENAI_API_KEY)
    chain_llm = llm.get_chain()

    while True:
        input_text = input("Enter the process description: ")
        res = chain_llm.invoke({"input": input_text})
        print(res)
    
"""
The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.
"""