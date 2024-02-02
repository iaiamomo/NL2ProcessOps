from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import Runnable, RunnableLambda, RunnablePassthrough, RunnableParallel, RunnableBranch
import dotenv
import os
import re


TEMPLATE = """You are a very proficient assistant expert in Business Process Management tasks. You are able to extract the process model in mermaid.js from a process description. To generate the process model you should extract the start event, end event, task, exclusive gateway and parallel gateway from the process description.

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
All nodes are connected with each other with the help of the direction.
    direction: -->
If there are some conditions or annotations it is necessary to use text on links (i.e., edge labels)
    edge label: |condition or annotation|
Edge label is always located between 2 nodes: id:exclusivegateway:{{x}} --> |condition or annotation|id:task:(task label)

Include the mermaid.js process model within the ```mermaid and ``` markdown delimiters after the "Answer:" line. Do not add any other text, only mermaid.js code block.

Create the process model in mermaid.js for the following process description: {input}
Answer:
"""


class CustomOutputParser(StrOutputParser):
    """The output parser for the LLM."""
    def parse(self, text: str) -> str:
        # remove any newline character at the beginning and at the end of the string
        text = text.strip("\n")
        # remove any whitespace at the beginning and at the end of the string
        text = text.strip()
        # parse the output of the LLM
        """Parse the output of an LLM call."""
        # check that the string starts with a triple backtick followed by "py"
        # and ends with a triple backtick
        if not text.startswith("```mermaid"):
            print(text)
            raise ValueError("The string should start with a triple backtick followed by python")
        if not text.endswith("```"):
            print(text)
            raise ValueError("The string should end with a triple backtick")
        # remove the triple backticks at the beginning and at the end and return the string
        # use the strip method to remove the triple backticks
        return text.strip("```mermaid").strip()

class MermaidLLM:

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = PromptTemplate.from_template(TEMPLATE)
        self.output_parser = CustomOutputParser()

    def get_chain(self) -> str:
        chain = self.prompt | self.model | self.output_parser
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