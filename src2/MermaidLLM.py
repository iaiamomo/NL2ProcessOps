from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import dotenv
import os

TEMPLATE = """You are a very proficient assistant expert in Business Process Management tasks. You are able to extract the process model in mermaid.js from a process description. first you should extract the start event, end event, task, exclusive gateway and parallel gateway from the process description. Then you can generate the process model.

Rules for mermaid js flowcharts:
The graph must use the LR (Left to Right) direction.
Each mermaid js node must have the following structure:
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
All nodes that have occurred more than once should have following structure: id:type: (i.e., 2:task:) by futher occurrence. It is strictly prohibited to use only id (i.e. 2) as a reference.
All nodes are connected with each other with the help of the direction.
    direction: --> 
If there are some conditions or annotations it is necessary to use text on links (i.e., edge labels)
    edge label: |condition or annotation|
Edge label is always located between 2 nodes: id:exclusivegateway:{{x}} --> |condition or annotation|id:task:(task label)

Include the mermaid.js inside markdown code block:
```mermaid
```
Do not add any other text. Only mermaid.js code block.

Create a flow diagram in mermaid.js for the following process description: {input}
"""


class MermaidLLM:

    def __init__(self, openai_key):
        self.model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0.0)

        # 2. define the prompt to use
        self.prompt = PromptTemplate.from_template(TEMPLATE)

        self.output_parser = StrOutputParser()

        self.chain = self.prompt | self.model | self.output_parser

if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm = MermaidLLM(OPENAI_API_KEY)

    while True:
        input_text = input("Enter the process description: ")
        res = llm.chain.invoke({"input": input_text})
        print(res)