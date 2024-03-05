from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import dotenv
import os


TEMPLATE = """You are a very proficient assistant expert in Python programming.

You are given in input a Python code that you need to revise.

The Python code could contain thread execution, if statements, for loops, while loops, functions, classes, and other Python programming constructs.

You need to revise the Python code as follows:
- in case of threads execution, if the threds are executed in parallel, you need to add the invocation parallel() before the thread execution and end_parallel() after the thread execution
- in case of if statements, you need to put the condition inside the check() function
- in case of invocation the call() method for a class, put the invocation to the service "http://localhost:5000/<name_of_the_class>" with the method POST and the body containing the input of the function
- do not add other code, just revise the code as described above

Here is the Python code that you need to revise: {input}
Response:
"""

class DeployLLM():

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = PromptTemplate.from_template(TEMPLATE)
        self.output_parser = StrOutputParser()

    def get_chain(self):
        chain = self.prompt | self.model | self.output_parser
        return chain

if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo-16k"
    model = "gpt-4-0125-preview"
    llm = DeployLLM(model, OPENAI_API_KEY)

    p_code = "llm_process_code.py"
    with open(p_code, "r") as f:
        code = f.read()
    
    chain = llm.get_chain()
    output = chain.invoke({"input": code})
    print(output)
