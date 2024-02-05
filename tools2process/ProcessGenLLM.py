from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import importlib.util
import os
import dotenv
import random

TEMPLATE = """Provide me a process description in the industrial manufacturing domain.

The actors involved in the process must be:
{actors}

The tasks that must be performed are:
{tasks}

The process description needs to be a single paragraph and must be discorsive and coherent with the actors and tasks provided. Do not provide the list of tasks and actors, but a discorsive and coherent paragraph.
"""


class ToolDict:

    @staticmethod
    def summary(cls):
        return {cls.__name__: {
            'description': f"{cls.description['description']}",
            'actor': cls.description['actor']
        }}

    def __init__(self):
        self.tools_dir = ('./tools')
        self.tools = []
        self.except_files = ['__init__.py', '__pycache__']
        for file in os.listdir(self.tools_dir):
            if file.endswith('.py') and file not in self.except_files:
                actor_file = file.split('.')[0]
                basename = os.path.basename(self.tools_dir)
                module = importlib.import_module(f'{basename}.{actor_file}')
                classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
                for cls in classes:
                    self.tools.append(ToolDict.summary(cls))


class GeneratorLLM:

    def __init__(self, model="gpt-3.5-turbo", openai_key=None, temperature=0.0):
        #model = "gpt-4"
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = PromptTemplate.from_template(TEMPLATE)
        self.output_parser = StrOutputParser()

    def get_chain(self):
        return self.prompt | self.model | self.output_parser


def generate_process_description():
    dotenv.load_dotenv()
    generator = GeneratorLLM(openai_key=os.getenv('OPENAI_API_KEY'))
    tools_manager = ToolDict()

    tools = tools_manager.tools
    random.shuffle(tools)

    tools_to_include = tools[:6]
    print(tools_to_include)

    actors = ""
    tasks = ""
    for tool in tools_to_include:
        tool_key = list(tool.keys())[0]
        actors += f"{tool[tool_key]['actor']}, "
        tasks += f"{tool[tool_key]['description']}, "
    actors = actors[:-2]
    tasks = tasks[:-2]

    res = generator.get_chain().invoke({"actors": actors, "tasks": tasks})
    print(res)


if __name__ == '__main__':
    generate_process_description()
