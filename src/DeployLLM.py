from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser
import dotenv
import os


TEMPLATE = """You are a very proficient assistant expert in Python programming.

You are given in input a Python code that you need to revise.

The Python code could contain thread execution, if statements, for loops, while loops, functions, classes, and other Python programming constructs.

You need to revise the Python code as follows:
- in case of invocation of threads, if the threds are executed in parallel, you need to add the invocation parallel() before the thread execution and end_parallel() after the thread execution.
- in case of if statements, you need to put the condition inside the check() function. e.g., if "if a > b:" is called, you need to replace it with "check(a > b):"
- do not add other code, just revise the code as described above

Here is the Python code that you need to revise: {code_r}
Response:
"""

class CustomOutputParser(BaseOutputParser):
    """The output parser for the LLM."""
    def parse(self, text: str) -> str:
        text = text.strip("\n")
        text = text.strip()
        # count how many ``` are in the text
        back_count = text.count("```")
        if back_count != 2:
            print(text)
            raise ValueError("The string should contain exactly two triple backticks")
        code = text.split("```")[1]
        code = code.strip().strip("python").strip()
        #print(code)
        return code


class DeployLLM():

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = PromptTemplate.from_template(TEMPLATE)
        self.output_parser = CustomOutputParser()

    def get_chain(self):
        chain = self.prompt | self.model | self.output_parser
        return chain

if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo-16k"
    model = "gpt-4-0125-preview"
    llm = DeployLLM(model, OPENAI_API_KEY)

    p_code = "p01_gpt4.py"
    with open(p_code, "r") as f:
        code = f.read()
    
    chain = llm.get_chain()
    output = chain.invoke({"code_r": code})
    print(output)
