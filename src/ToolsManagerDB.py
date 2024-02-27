from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import importlib.util
import os
import dotenv
import json


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

    def embed_tools(self, embedding_function):
        self.embedding_function = embedding_function
        self.db = Chroma.from_texts(self.tools, embedding_function)

    # cls is for instance "capture_image"
    def extract_input_output(self, cls, file_name):
        tool_info = {}
        basename = os.path.basename(self.tools_dir)
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
        list_match = []
        try:
            # cosine distance is used to find the closest vector
            # best_match contains the list of the closest vectors (the first element is the closest one)
            best_match = self.db.similarity_search_with_score(keywords)
            print(f"best_match: {best_match}")
            for i in range(len(best_match)):
                match_elem = best_match[i]
                # if the first element is already above 0.4, we don't need to check the rest
                if i == 0 and match_elem[1] >= 0.4:
                    break
                # if the first element is below 0.4, we count it
                # it the rest of the elements are below 0.2, we count them
                elif i == 0 and match_elem[1] < 0.4:
                    tool_name = match_elem[0].page_content.split(' ')[0]
                    file_name = match_elem[0].page_content.split(' ')[1]
                    api_info = self.extract_input_output(tool_name, file_name)
                    list_match.append(api_info)
                    #print(f"\tname: {match_elem} score: {match_elem[1]}")
                elif i > 0 and match_elem[1] <= 0.2:
                    tool_name = match_elem[0].page_content.split(' ')[0]
                    file_name = match_elem[0].page_content.split(' ')[1]
                    api_info = self.extract_input_output(tool_name, file_name)
                    list_match.append(api_info)
                    #print(f"\tname: {match_elem} score: {match_elem[1]}")
        except Exception as e:
            exception = str(e)
            print(f"Exception: {exception}")
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': None, 'exception': exception}
        else:
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': list_match, 'exception': None}


class ToolsManagerDB:

    def __init__(self, openai_key):
        self.tool_store = ToolStore(openai_key)
        embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=openai_key)
        self.tool_store.embed_tools(embedding_function)

    def command_line(self):
        while True:
            tool_keywords = input('Please enter the KEYWORDS for the tool you want to use (\'exit\' to exit):\n')
            if tool_keywords == 'exit':
                break
            response = self.tool_store.search(tool_keywords)['output']
            for elem in response:
                print('The tool you want to use is: \n' + elem['name'] + '\n' + json.dumps(elem))
            '''while True:
                command = input('Please enter the PARAMETERS for the tool you want to use (\'exit\' to exit): \n')
                if command == 'exit':
                    break
                else:
                    command = command.replace(' ', '')
                    processed_parameters = command.split(',')
                    print(f"tool: {response['output']['name']} with ({processed_parameters})")'''


if __name__ == '__main__':
    dotenv.load_dotenv()
    openai_key = os.getenv('OPENAI_API_KEY')
    tools_manager = ToolsManagerDB(openai_key=openai_key)
    tools_manager.command_line()
