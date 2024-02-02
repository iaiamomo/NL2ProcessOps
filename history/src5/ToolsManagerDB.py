from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
import importlib.util
import os
import dotenv
import json

# TODO: decide if we want to search using similarity_search_with_score that output the score of the similarity

class ToolStore():
    
    @staticmethod
    def tool_summary(cls, file_name):
        return cls.__name__ + " " + file_name + " " + cls.description['description']

    def __init__(self, openai_key):
        self.tools_dir = ('./tools')
        self.openai_key = openai_key
        self.classes_tools = []
        self.tools = []
        self.except_files = ['__init__.py', '__pycache__']
        for file in os.listdir(self.tools_dir):
            if file.endswith('.py') and file not in self.except_files:
                actor_file = file.split('.')[0]
                basename = os.path.basename(self.tools_dir)
                module = importlib.import_module(f'{basename}.{actor_file}')
                classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
                for cls in classes:
                    self.classes_tools.append(cls)
                    self.tools.append(ToolStore.tool_summary(cls, actor_file))

        self.db = FAISS.from_texts(self.tools, OpenAIEmbeddings(api_key=self.openai_key))

    # cls is for instance "capture_image"
    def extract_input_output(self, cls, file_name):
        tool_info = {}
        basename = os.path.basename(self.tools_dir)
        # loop through all the files in the tools directory
        module = importlib.import_module(f'{basename}.{file_name}')
        tool_class = getattr(module, cls)
        tool_info = {
            'name': tool_class.__name__,
            'description': tool_class.description['description'] + tool_class.description['more details'],
            'input_parameters': tool_class.description['input_parameters'],
            'output_parameters': tool_class.description['output_parameters'],
            'actor': tool_class.description['actor']
        }
        return tool_info


    def search(self, keywords):
        # Searches for relevant tools in various libraries based on the keyword.
        input_parameters = {
            'keywords': keywords
        }
        try:
            #keywords = OpenAIEmbeddings(api_key=self.openai_key).embed_query(keywords)
            # L2 distance is used to find the closest vector (Euclidean distance)
            #best_match = self.db.similarity_search_by_vector(keywords)[0]
            best_match = self.db.similarity_search_with_score(keywords)
            #for i in range(len(best_match)):
            #    print(f"name: {best_match[i][0]} score: {best_match[i][1]}")
            best_match = best_match[0][0]
            tool_name = best_match.page_content.split(' ')[0]
            file_name = best_match.page_content.split(' ')[1]
            api_info = self.extract_input_output(tool_name, file_name)
        except Exception as e:
            exception = str(e)
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': None, 'exception': exception}
        else:
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': api_info, 'exception': None}


class ToolsManagerDB:

    def __init__(self, openai_key):
        self.tool_store = ToolStore(openai_key)

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
    dotenv.load_dotenv()
    openai_key = os.getenv('OPENAI_API_KEY')
    tools_manager = ToolsManagerDB(openai_key=openai_key)
    tools_manager.command_line()