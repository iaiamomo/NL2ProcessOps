from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import dotenv
import os

TEMPLATE = """You are a very proficient assistant expert in Business Process Management.

You are able to better describe the list of tasks-activities from a process description. 
To generate the revised list of tasks-activities you have access to an already generated list of tasks-activities. The list of tasks-activities is specified after the "Tasks:" line.

The output is a list of strings. Each string contains a summarization of an task-activities.

Here are a few examples of process descriptions and the expected output:
1. Process description: Plastic injection molding is a manufacturing process for producing a variety of parts by injecting molten plastic material into a mold, and letting it cool and solidify into the desired end product. Our interest is in the quality assurance process which involves real-time monitoring of injection molding parameters. As each batch of molten plastic enters the mold, sensors capture data on temperature, pressure, and fill rates. The system analyzes this data to ensure that the molding parameters align with the specified standards. If any deviations are detected, the system triggers adjustments to the injection molding machine settings, allowing for immediate correction. Once the parameters are within the acceptable range, the system authorizes the production run to continue. This dynamic monitoring process guarantees the consistency and quality of the plastic molded components, minimizing the risk of defects and ensuring adherence to precise manufacturing specifications.
   Tasks: ["enter mold", "capture sensor", "analysis", "machine adjusted", "plastic produced"]
   Response: ["batch of molten plastic enters the mold", "sensors capture temperature, pressure, anf fill rates of machine", "analysis of measured data", "settings of machine are adjusted", "plastic molded components are produced"]

2. Process description: The warehouse of Grimaldi is a warehouse that stores cardboard rolls. A cardboard roll is used to produce cardboards. There exists two types of cardboard: the white cardboard and the brown cardboard. The warehouse stores the cardboard rolls depending on the type of cardboard. When a new cardboard roll arrives at the warehouse, the worker checks the type of cardboard and enter this information inside the WMS system. The system automatically capture an image of the current status of the warehouse. By analyzing the image, the system identifies the location where the cardboard roll should be stored. Then the worker stores the cardboard rool in the warehouse and the system updates the quantity of that cardboard rolls in the warehouse.
   Tasks: ["check type of cardboard", "enter information", "capture image", "identify location", "store", "update the quantity"]
   Response: ["the worker checks the type of cardboard", "the worker enters the information inside the WMS system", "the system captures an image of the current status of the warehouse", "the system identifies the location where the cardboard roll should be stored", "the worker stores the cardboard rool in the warehouse", "the system updates the quantity of that cardboard rolls in the warehouse"]

3. Process description: The production of custom metal brackets begins with order processing. The warehouse department evaluates the parts lists and in parallel the production planning department configures the robotic assembly line accordingly. The automated precision machine cuts the metal and the welding machine assembles the parts into brackets. A computer vision inspection system then checks for quality assurance. If defective brakets are detected, the process ends. After inspection, a coating system enhances durability. Finally, the process is complete.
   Tasks: ["process order", "evaluate parts", "configure assembly line", "cut metal", "weld metal", "inspect quality", "coat brackets"]
   Response: ["processing of the custom metal braket order", "evaluation of parts from warehouse", "configuration of the robotic assembly line", "cut the metal", "weld the metal part", "quality inspection of the produced brackets", "coating of the produced brackets"]

Process description: {input}
Tasks: {tasks}
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
   model = "gpt-3.5-turbo"
   #model = "gpt-4"
   llm = TaskRetrieverLLM(model, OPENAI_API_KEY)
   chain_llm = llm.get_chain()

   while True:
      #input_text = input("Enter the process description: ")
      res = chain_llm.invoke({"input": "order for a spindle arrives at the sales department, a new process instance is initiated. The warehouse system retrive the necessary raw materials, and in parallel the L12 lines is set up for the assembly of the ordered spindle. Once the warehouse successfully retrieves the raw materials and the L12 line is set up, the spindle is assembled over the L12 line. Subsequently, the spindle undergoes testing and running-in in the smart tester. If the outcome of the test is negative, the spindle is sent to maintenance. Then, the the process ends.", "tasks":['new order for a spindle arrives', 'retrieval of raw materials', 'set up of L12 line', 'assembly of the spindle', 'testing and running-in of the spindle', 'maintenance of the spindle']})
      print(res)
      input()

"""
The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.

['capture photo of cardboard', 'analyze photo', 'set speed of die cutting machine to 10000 RPM']
['continuously capturing a photo of the cardboard being produced', 'analyzing each photo to check if all the markers identified are ok', 'setting the speed of the die cutting machine to 10000 RPM']

The manufacturing process of spindles in HSD company is fully automated. When a new order for a spindle arrives at the sales department, a new process instance is initiated. The warehouse system retrive the necessary raw materials, and in parallel the L12 line is set up for the assembly of the ordered spindle. Once the warehouse successfully retrieves the raw materials and the L12 lines is set up, the spindle is assembled over the L12 lines. Subsequently, the spindle undergoes testing and running-in in the smart tester. If the outcome of the test is negative, the spindle is sent to maintenance. Then, the the process ends.

['new order for a spindle arrives', 'retrieval of raw materials', 'set up of L12 line', 'assembly of the spindle', 'testing and running-in of the spindle', 'maintenance of the spindle']
['a new order for a spindle arrives at the sales department', 'the warehouse system retrieves the necessary raw materials', 'the L12 line is set up for the assembly of the ordered spindle', 'the spindle is assembled over the L12 line', 'the spindle undergoes testing and running-in in the smart tester', 'if the outcome of the test is negative, the spindle is sent to maintenance', 'the process ends']
"""