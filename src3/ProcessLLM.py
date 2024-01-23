from TaskRetrieverLLM import TaskRetrieverLLM
from ToolsManagerDB import ToolsManagerDB
from DataLLM import DataLLM
from CodeLLM import CodeLLM

class ProcessLLM:

    def __init__(self, model, openai_key, temperature=0.0):
        # task retriever
        tr_llm = TaskRetrieverLLM(model=model, openai_key=openai_key, temperature=temperature)
        self.tr_chain = tr_llm.get_chain()

        # code generator
        cg_llm = CodeLLM(model=model, openai_key=openai_key, temperature=temperature)
        self.cg_chain = cg_llm.get_chain()

        

    def get_chain(self):
        chain = (

        )
        return chain