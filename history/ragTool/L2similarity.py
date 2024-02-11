from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
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

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")   # default model of chroma DB
        #embedding_function = OpenAIEmbeddings(api_key=self.openai_key)
        self.db = FAISS.from_texts(self.tools, embedding_function)

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
            #keywords = OpenAIEmbeddings(api_key=self.openai_key).embed_query(keywords)
            #best_match = self.db.similarity_search_by_vector(keywords)[0]

            # L2 distance is used to find the closest vector (Euclidean distance)
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
                    print(f"name: {match_elem} score: {match_elem[1]}")
                    break
                elif i > 0 and match_elem[1] <= 0.2:
                    tool_name = match_elem[0].page_content.split(' ')[0]
                    file_name = match_elem[0].page_content.split(' ')[1]
                    api_info = self.extract_input_output(tool_name, file_name)
                    list_match.append(api_info)
                    print(f"name: {match_elem} score: {match_elem[1]}")
        except Exception as e:
            exception = str(e)
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': None, 'exception': exception}
        else:
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': list_match, 'exception': None}


class ToolsManagerDB:

    def __init__(self, openai_key):
        self.tool_store = ToolStore(openai_key)

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


"""
The calibration process of a cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die cutting machine is set to 10000 RPM and the process ends.

['capture photo of cardboard', 'analyze photo', 'set speed of die cutting machine to 10000 RPM']
['continuously capturing a photo of the cardboard being produced', 'analyzing each photo to check if all the markers identified are ok', 'setting the speed of the die cutting machine to 10000 RPM']

The manufacturing process of spindles in HSD company is fully automated. When a new order for a spindle arrives at the sales department, a new process instance is initiated. The warehouse system retrive the necessary raw materials, and in parallel the L12 line is set up for the assembly of the ordered spindle. Once the warehouse successfully retrieves the raw materials and the L12 lines is set up, the spindle is assembled over the L12 lines. Subsequently, the spindle undergoes testing and running-in in the smart tester. If the outcome of the test is negative, the spindle is sent to maintenance. Then, the the process ends.

['new order for a spindle arrives', 'retrieval of raw materials', 'set up of L12 line', 'assembly of the spindle', 'testing and running-in of the spindle', 'maintenance of the spindle']
['a new order for a spindle arrives at the sales department', 'the warehouse system retrieves the necessary raw materials', 'the L12 line is set up for the assembly of the ordered spindle', 'the spindle is assembled over the L12 line', 'the spindle undergoes testing and running-in in the smart tester', 'if the outcome of the test is negative, the spindle is sent to maintenance', 'the process ends']
"""