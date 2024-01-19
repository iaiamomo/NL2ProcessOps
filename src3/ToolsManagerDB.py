from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
import importlib.util
import os
import dotenv
import json

class ToolStore():
    
    @staticmethod
    def tool_summary(cls):
        cls_name = cls.__name__
        # split cls_name by capital letters
        cls_name = ''.join(['_' + i.lower() if i.isupper() else i for i in cls_name]).strip("_")
        return cls_name + " " + cls.description 

    def __init__(self, openai_key):
        self.tools_dir = ('./tools')
        self.openai_key = openai_key
        self.classes_tools = []
        self.tools = []
        except_files = ['__init__.py', '__pycache__']
        for file in os.listdir(self.tools_dir):
            if file.endswith('.py') and file not in except_files:
                api_file = file.split('.')[0]
                basename = os.path.basename(self.tools_dir)
                module = importlib.import_module(f'{basename}.{api_file}')
                classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
                for cls in classes:
                    self.classes_tools.append(cls)
                    self.tools.append(ToolStore.tool_summary(cls))

        self.db = FAISS.from_texts(self.tools, OpenAIEmbeddings(api_key=self.openai_key))

    # cls is for instance "capture_image"
    def extract_input_output(self, cls):
        basename = os.path.basename(self.tools_dir)
        print(basename)
        api_file = cls
        print(api_file)
        module = importlib.import_module(f'{basename}.{api_file}')
        # retrieve only classes of the api_file module
        classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
        for cls in classes:
            api_info = {
                'name': cls.__name__,
                'description': cls.description,
                'input_parameters': cls.input_parameters,
                'output_parameters': cls.output_parameters
            }
        return api_info


    def search(self, keywords):
        # Searches for relevant tools in various libraries based on the keyword.
        input_parameters = {
            'keywords': keywords
        }
        try:
            keywords = OpenAIEmbeddings(api_key=self.openai_key).embed_query(keywords)
            best_match = self.db.similarity_search_by_vector(keywords)[0]
            api_file_name = best_match.page_content.split(' ')[0]
            api_info = self.extract_input_output(api_file_name)
        except Exception as e:
            exception = str(e)
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': None, 'exception': exception}
        else:
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': api_info, 'exception': None}


class ToolsManagerDB:

    def __init__(self):
        dotenv.load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.tool_store = ToolStore(OPENAI_API_KEY)

    def command_line(self):
        while True:
            tool_keywords = input('Please enter the KEYWORDS for the tool you want to use (\'exit\' to exit):\n')
            if tool_keywords == 'exit':
                break
            response = self.tool_store.search(tool_keywords)
            print('The tool you want to use is: \n' + response['output']['name'] + '\n' + json.dumps(response['output']))
            while True:
                command = input('Please enter the PARAMETERS for the tool you want to use (\'exit\' to exit): \n')
                if command == 'exit':
                    break
                else:
                    command = command.replace(' ', '')
                    processed_parameters = command.split(',')
                    print(f"tool: {response['output']['name']} with ({processed_parameters})")


if __name__ == '__main__':
    tools_manager = ToolsManagerDB()
    tools_manager.command_line()