from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableLambda
import dotenv
import os
import re


TEMPLATE = """You are a very proficient assistant expert in Business Process Management. 

You are able to extract the process model in mermaid.js from a process description. To generate the process model you should extract the start event, end event, task, exclusive gateway and parallel gateway from the process description.
Each model has only one start event, one or more end events, activities (also called tasks), and gateways.
A start event shows where a process begins. It has solely one outgoing element and no incoming elements. An end event marks where a process ends. It has one incoming element and no outgoing elements.
There are multiple tasks and paths between start and end events.
A path through the process model represents one of the variants of how the process could be executed.
Tasks represent the work performed within a process. A task will normally take some time to perform, involve one or more resources, require some type of input and produce some sort of output. Each task has a label.
Gateways are modeling elements that control the flow of work through the paths of the process. Gateways themselves are not activities. They just split and merge the process flow. Gateways are unnecessary if the process flow does not require controlling. The two most commonly used gateways are the exclusive and parallel gateways.
If, after some particular task, a decision is to be made (i.e. alternative paths occur), a splitting exclusive gateway is to be used. Only one of multiple outgoing paths will be (exclusively) executed. After that, the process flow should be merged again with the help of a merging exclusive gateway.
If, after some particular task, multiple tasks should be executed at the same time, a splitting parallel gateway is to be used. After the execution of parallel tasks, there is always a synchronization point (waiting for several separate paths to reach a certain point before the process can continue). This synchronization point is represented by a merging parallel gateway.
Every split in a control flow should always be merged. Only gateways of the same type could be used for splitting and merging.

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
1. Process description: When building a custom machine out of Lego bricks, you first need to develop the basic design. After that, you order certain Lego brick sets. You give the lego sets to a group of children which should sort the parts for you (into a number of containers). Your machine is built out of a number of subcomponents. You build them individually, using parts from the sorted containers.  If there are no more parts in a container, you reorder individual parts. After building each subcomponent, you have to test them individually and (if each test is successful) assemble them. If subcomponents are not tested successfully, you have to redesign and rebuild them.
   Response: ```mermaid
   graph LR
    1:startevent:((startevent)) --> 2:task:(Develop Basic Design)
    2:task: --> 3:task:(Order Lego Brick Sets)
    3:task: --> 4:task:(Sort Lego Parts)
    4:task: --> 5:task:(Build Subcomponents)
    5:task: --> 6:exclusivegateway:{{x}}
    6:exclusivegateway:{{x}} --> |No more parts| 7:task:(Reorder Parts)
    7:task: --> 5:task: 
    6:exclusivegateway:{{x}} --> |Parts available| 8:task:(Test Subcomponents)
    8:task: --> 9:exclusivegateway:{{x}}
    9:exclusivegateway:{{x}} --> |Test Failed| 10:task:(Redesign and Rebuild)
    10:task: --> 8:task: 
    9:exclusivegateway:{{x}} --> |Test Successful| 11:task:(Assemble Subcomponents)
    11:task: --> 12:endevent:((endevent))
   ```
   ```tasks
   ["develop the basic design of the machine", "order the required Lego brick sets", "sort the Lego parts into containers", "build the subcomponents of the machine", "test each subcomponent", "if a test fails, redesign and rebuild the subcomponent", "if all tests are successful, assemble the subcomponents", "if there are no more parts in a container, reorder individual parts"]
    ```

2. Process description: You produce custom chainsaws on demand. Your chainsaws have at least 5 properties such as length of the "guide bar" (Schwertlaenge), chain width, electric or motor chainsaw. After your customer told you the properties, you can start ordering the parts from various online sources (in parallel). After the parts arrive you have to do a manual inspection of all parts, and then assemble the parts. During production, you regularly send updates to your customer. After producing the first saw you send it to your customer. If he likes it, the rest of his order are produced.
   Response: ```mermaid
   graph LR
   1:startevent:((startevent)) --> 2:task:(Customer provides chainsaw properties)
   2:task: --> 3:parallelgateway:{{AND}}
   3:parallelgateway:{{AND}} --> 4:task:(Order guide bar)
   3:parallelgateway:{{AND}} --> 5:task:(Order chain width)
   3:parallelgateway:{{AND}} --> 6:task:(Order chainsaw type)
   4:task: --> 7:parallelgateway:{{AND}}
   5:task: --> 7:parallelgateway:{{AND}}
   6:task: --> 7:parallelgateway:{{AND}}
   7:parallelgateway:{{AND}} --> 8:task:(Inspect parts)
   8:task: --> 9:task:(Assemble chainsaw)
   9:task: --> 10:task:(Send updates to customer)
   10:task: --> 11:task:(Send first chainsaw to customer)
   11:task: --> 12:exclusivegateway:{{x}}
   12:exclusivegateway:{{x}} --> |Customer likes it| 13:task:(Produce rest of order)
   12:exclusivegateway:{{x}} --> |Customer doesn't like it| 14:task:(Adjust chainsaw properties)
   13:task: --> 15:endevent:((endevent))
   14:task: --> 2:task:
   ```
   ```tasks
   ["receive the properties of the chainsaw from the customer", "order guide bar", "order chain width", "order chainsaw type", "inspect all parts manually", "assemble the parts", "send regular updates to the customer during production", "produce the first saw and send it to the customer", "if the customer likes the first saw, produce the rest of the order"]

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
    # gpt-3.5-turbo-16k
    # gpt-4
    # gpt-4-0125-preview
    model = "gpt-4-0125-preview"
    llm = MermaidLLM(model, OPENAI_API_KEY)
    chain_llm = llm.get_chain()

    while True:
        input_text = input("Enter the process description: ")
        res = chain_llm.invoke({"input": input_text})
        print(f"Mermaid process model:\n{res['model']}\n")
        print(f"Tasks:\n{res['tasks']}")