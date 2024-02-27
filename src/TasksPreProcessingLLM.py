from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


TEMPLATE = """You are a very proficient assistant expert in Business Process Management.

You are able to better describe the list of tasks-activities from a process description. 
To generate the revised list of tasks-activities you have access to an already generated list of tasks-activities. The list of tasks-activities is specified after the "Tasks:" line.

The output is a list of strings. Each string contains a summarization of an task-activities.

Here are a few examples of process descriptions and the expected output:
1. Process description: Plastic injection molding is a manufacturing process for producing a variety of parts by injecting molten plastic material into a mold, and letting it cool and solidify into the desired end product. Our interest is in the quality assurance process which involves real-time monitoring of injection molding parameters. As each batch of molten plastic enters the mold, sensors capture data on temperature, pressure, and fill rates. The system analyzes this data to ensure that the molding parameters align with the specified standards. If any deviations are detected, the system triggers adjustments to the injection molding machine settings, allowing for immediate correction. Once the parameters are within the acceptable range, the system authorizes the production run to continue. This dynamic monitoring process guarantees the consistency and quality of the plastic molded components, minimizing the risk of defects and ensuring adherence to precise manufacturing specifications.
   Tasks: ["enter mold", "capture sensor", "analysis", "if deviations are detected, adjust machine", "plastic produced"]
   Response: ["batch of molten plastic enters the mold", "sensors capture temperature, pressure, anf fill rates of machine", "analysis of measured data", "settings of machine are adjusted", "plastic molded components are produced"]

2. Process description: When building a custom machine out of Lego bricks, you first need to develop the basic design. After that, you order certain Lego brick sets. You give the lego sets to a group of children which should sort the parts for you (into a number of containers). Your machine is built out of a number of subcomponents. You build them individually, using parts from the sorted containers. If there are no more parts in a container, you reorder individual parts. After building each subcomponent, you have to test them individually and (if each test is successful) assemble them. If subcomponents are not tested successfully, you have to redesign and rebuild them.
   Tasks: ["develop the design", "order", "sort parts", "build", "if there are no parts, reorder part", "test", "if subcomponents are not tested successfully, redesign and rebuild", "assemble", "reorder parts"]
   Response: ["develop the basic design of the machine", "order the required Lego brick sets", "sort the Lego parts into containers", "build the subcomponents of the machine", "reorder part", "test each subcomponent", "redesigning and rebuilding the subcomponent", "assemble the subcomponents", "reorder individual parts"]

3. Process description: You produce custom chainsaws on demand. Your chainsaws have at least 5 properties such as length of the "guide bar" (Schwertlaenge), chain width, electric or motor chainsaw. After your customer told you the properties, you can start ordering the parts from various online sources (in parallel). After the parts arrive you have to do a manual inspection of all parts, and then assemble the parts. During production, you regularly send updates to your customer. After producing the first saw you send it to your customer. If he likes it, the rest of his order are produced.
   Tasks: ["receive the properties", "order guide bar", "order chain width", "order chainsaw type", "inspect", "assemble", "send updates", "produce", "send to the customer", "if he likes it, produce the rest"]
   Response: ["receive the properties of the chainsaw from the customer", "order guide bar", "order chain width", "order chainsaw type", "manual inspect all parts", "assemble the parts", "send regular updates to the customer during production", "send chainsaw to the customer", "produce the rest of the order"]

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

