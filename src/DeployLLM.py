from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import dotenv
import os
import tokenize
from io import StringIO


TEMPLATE = """You are a very proficient assistant expert in Python programming.

You are given in input a Python code that you need to revise.

The Python code could contain thread execution, if statements, for loops, while loops, functions, classes, and other Python programming constructs.

You need to revise the Python code as follows:
- in case of invocation of threads, if the threds are executed in parallel, you need to add the invocation parallel() before the thread execution and end_parallel() after the thread execution.
- in case of if statements, you need to put the condition inside the check() function. e.g., if "if a > b:" is called, you need to replace it with "check(a > b):"
- do not add other code, just revise the code as described above

Here is the Python code that you need to revise: {input}
Response:
"""

def remove_comments_and_docstrings(source):
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
        # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    temp=[]
    for x in out.split('\n'):
        if x.strip()!="":
            temp.append(x)
    return '\n'.join(temp)

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

    p_code = "p01_gpt4.py"
    with open(p_code, "r") as f:
        code = f.read()
    new_code = remove_comments_and_docstrings(code)
    
    chain = llm.get_chain()
    output = chain.invoke({"input": new_code})
    print(output)
