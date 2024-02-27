from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import importlib.util
import os
import dotenv
import random


TEMPLATE = """Provide me a process description in the industrial manufacturing domain.

Examples of manufacturing process descriptions:
- Plastic injection molding is a manufacturing process for producing a variety of parts by injecting molten plastic material into a mold, and letting it cool and solidify into the desired end product. Our interest is in the quality assurance process which involves real-time monitoring of injection molding parameters. As each batch of molten plastic enters the mold, sensors capture data on temperature, pressure, and fill rates. The system analyzes this data to ensure that the molding parameters align with the specified standards. If any deviations are detected, the system triggers adjustments to the injection molding machine settings, allowing for immediate correction. Once the parameters are within the acceptable range, the system authorizes the production run to continue. This dynamic monitoring process guarantees the consistency and quality of the plastic molded components, minimizing the risk of defects and ensuring adherence to precise manufacturing specifications.
- The production of custom metal brackets begins with order processing. The warehouse department evaluates the parts lists and in parallel the production planning department configures the robotic assembly line accordingly. The automated precision machine cuts the metal and the welding machine assembles the parts into brackets. A computer vision inspection system then checks for quality assurance. If defective brakets are detected, the process ends. After inspection, a coating system enhances durability. Finally, the process is complete.

You need to provide a manufacturing process description that involves the following actors and tasks:
{actors_tasks}

Guidelines:
- Each actor is responsible to perform the relative task
- The process description must contain the tasks and actors provided following a coherent control flow (e.g., if the actor A performs the task 1, then the actor B performs the task 2, etc.)
- Include in the control flow exclusive or parallel tasks (e.g., if the actor A performs the task 1, then the actor B performs the task 2, or the actor C performs the task 3)
- The task must be performed with proper input value. Do not describe what the task does, and do not provide the type of the input (e.g., np.matrix, int, bool, etc.). Just report the tasks that must be performed with the proper input value (e.g., 100, image, true (ok), etc.)
- If the process includes products or materials, include the type of product or material
- The manufacturing process must be coherent with the actors and tasks provided
- Do not provide the list of tasks and actors, but a discorsive and coherent paragraph
- The lenght of the process description must be less than 200 words

The manufacturing process description is
"""


class ToolDict:

    @staticmethod
    def summary(cls):
        return {cls.__name__: {
            'description': f"{cls.description['description']} {cls.description['more details']}",
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
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        self.prompt = PromptTemplate.from_template(TEMPLATE)
        self.output_parser = StrOutputParser()

    def get_chain(self):
        return self.prompt | self.model | self.output_parser


def generate_process_description(tools):
    generator = GeneratorLLM(openai_key=os.getenv('OPENAI_API_KEY'))
    random.shuffle(tools)

    n_random_tools = random.randint(5, 15)
    tools_to_include = tools[:n_random_tools]

    actors_tasks = ""
    for tool in tools_to_include:
        tool_key = list(tool.keys())[0]
        actors_tasks += f"{tool[tool_key]['actor']}: {tool[tool_key]['description']}.\n"
    actors_tasks = actors_tasks[:-1]

    res = generator.get_chain().invoke({"actors_tasks": actors_tasks})


if __name__ == '__main__':
    dotenv.load_dotenv(dotenv_path="./gen.env")
    tools_manager = ToolDict()
    tools = tools_manager.tools
    for i in range(30):
        generate_process_description(tools)
