from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import Runnable, RunnableLambda, RunnablePassthrough, RunnableParallel, RunnableBranch
import dotenv
import os
import re

TEMPLATE = """You are a very proficient assistant expert in Business Process Management. 

You are able to extract the process model in mermaid.js from a process description. To generate the process model you should extract the start event, end event, task, exclusive gateway and parallel gateway from the process description.

The mermaid.js process model should be generated according to the following rules:
The graph must use the LR (Left to Right) direction.
Each mermaid node must have the following structure:
    id:type:shape and text
        id - it is a unique identifier. Integer from 1 to n. Each node has a unique identifier
        type - defines the type of the element regarding to BPMN 2.0 notation.
            possible types are: start event, end event, task, exclusive gateway and parallel gateway.
        Based on the type of the node following shapes and texts are to be used:
            startevent: ((startevent))     i.e., id:startevent:((startevent))
            endevent: ((endevent))       i.e., id:endevent:((endevent))
            task: (task label)             i.e., id:task:(task label)
            exclusivegateway: {{x}}          i.e., id:exclusivegateway:{{x}}
            parallelgateway: {{AND}}         i.e., id:exclusivegateway:{{AND}}
All nodes that have occurred more than once should have following structure: id:type: (i.e., 2:task:) by futher occurrence.
All nodes are connected with each other with the help of the direction.
    direction: -->
If there are some conditions or annotations it is necessary to use text on links (i.e., edge labels)
    edge label: |condition or annotation|
Edge label is always located between 2 nodes: id:exclusivegateway:{{x}} --> |condition or annotation|id:task:(task label)

You are able to list the extracted task. The output is a list of strings. Each string contains an high level description of a task.

Include the mermaid.js process model within the ```mermaid and ``` markdown delimiters. Include the list of tasks within the ```tasks and ``` markdown delimiters. Do not add any other text, only mermaid.js code block and list of tasks.

Here are a few examples of process descriptions and the expected output:
1. Process description: Plastic injection molding is a manufacturing process for producing a variety of parts by injecting molten plastic material into a mold, and letting it cool and solidify into the desired end product. Our interest is in the quality assurance process which involves real-time monitoring of injection molding parameters. As each batch of molten plastic enters the mold, sensors capture data on temperature, pressure, and fill rates. The system analyzes this data to ensure that the molding parameters align with the specified standards. If any deviations are detected, the system triggers adjustments to the injection molding machine settings, allowing for immediate correction. Once the parameters are within the acceptable range, the system authorizes the production run to continue. This dynamic monitoring process guarantees the consistency and quality of the plastic molded components, minimizing the risk of defects and ensuring adherence to precise manufacturing specifications.
   Response: ```mermaid
   graph LR
   1:startevent:((startevent)) --> 2:task:(Batch enter the mold)
   2:task: --> 3:task:(Sensor capture data on temperature, pressure, and fill rates)
   3:task: --> 4:exclusivegateway:{{x}}
   4:exclusivegateway: --> |deviations detected| 5:task:(Adjust injection molding machine settings)
   4:exclusivegateway: --> |no deviations detected| 6:exclusivegateway:{{x}}
   5:task: --> 6:exclusivegateway:
   6:exclusivegateway: --> 7:task:(Continue production run)
   7:task: --> 8:endevent:((endevent))
   ```
   ```tasks
   ["batch of molten plastic enters the mold", "sensors capture temperature, pressure, anf fill rates of machine", "analysis of measured data", "settings of machine are adjusted", "plastic molded components are produced"]
    ```

2. Process description: The production of custom metal brackets begins with order processing. The warehouse department evaluates the parts lists and in parallel the production planning department configures the robotic assembly line accordingly. The automated precision machine cuts the metal and the welding machine assembles the parts into brackets. A computer vision inspection system then checks for quality assurance. If defective brakets are detected, the process ends. After inspection, a coating system enhances durability. Finally, the process is complete.
   Response: ```mermaid
   graph LR
   1:startevent:((startevent)) --> 2:task:(Order processing)
   2:task: --> 3:parallelgateway:{{AND}}
   3:parallelgateway: --> 4:task:(Configure robotic assembly line)
   3:parallelgateway: --> 5:task:(Warehouse parts evaluation)
   4:task: --> 6:parallelgateway:{{AND}}
   5:task: --> 6:parallelgateway:{{AND}}
   6:parallelgateway: --> 7:task:(Cut metal)
   7:task: --> 8:task:(Weld parts)
   8:task: --> 9:task:(Computer vision inspection)
   9:task: --> 10:exclusivegateway:{{x}}
   10:exclusivegateway: --> |defective brackets| 12:exclusivegateway:{{x}}
   10:exclusivegateway: --> |no defective brackets| 11:task:(Coating system)
   11:task: --> 12:exclusivegateway:
   12:exclusivegateway: --> 13:endevent:((endevent))
   ```
   ```tasks
   ["processing of the custom metal braket order", "evaluation of parts from warehouse", "configuration of the robotic assembly line", "cut the metal", "weld the metal part", "quality inspection of the produced brackets", "coating of the produced brackets"]

Process description: {input}
Answer:
"""


class MermaidLLM:

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = PromptTemplate.from_template(TEMPLATE)
        self.output_parser = StrOutputParser()

    def extract_mermaid_and_tasks(self, markdown_string):

        # Extract Mermaid diagram
        mermaid_pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
        mermaid_match = mermaid_pattern.search(markdown_string)
        
        if mermaid_match:
            mermaid_diagram = mermaid_match.group(1).strip()
        else:
            mermaid_diagram = None
        
        # Extract tasks
        tasks_pattern = re.compile(r'```tasks\n(.*?)\n```', re.DOTALL)
        tasks_match = tasks_pattern.search(markdown_string)
        
        if tasks_match:
            tasks_list = tasks_match.group(1).strip()
        else:
            tasks_list = None

        result = {
            'model': mermaid_diagram,
            'tasks': tasks_list
        }

        print(result)

        return result

    def get_chain(self) -> str:
        chain = (
            self.prompt
            | self.model
            | self.output_parser
            | RunnableLambda(lambda x: self.extract_mermaid_and_tasks(x))
        )
        return chain


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo"
    #model = "gpt-4"
    llm = MermaidLLM(model, OPENAI_API_KEY)
    chain_llm = llm.get_chain()

    while True:
        input_text = input("Enter the process description: ")
        res = chain_llm.invoke({"input": input_text})
        print(f"Mermaid process model: {res}")