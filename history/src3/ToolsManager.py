from sentence_transformers import SentenceTransformer, util
import importlib.util
import os
import json

# sources taken from https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank

class ToolSearcher():

    def __init__(self):
        tools_dir = ('./tools')
        classes_tools = []
        except_files = ['__init__.py', '__pycache__']
        for file in os.listdir(tools_dir):
            if file.endswith('.py') and file not in except_files:
                api_file = file.split('.')[0]
                basename = os.path.basename(tools_dir)
                module = importlib.import_module(f'{basename}.{api_file}')
                classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
                for cls in classes:
                    classes_tools.append(cls)

        def tool_summary(cls):
            cls_name = cls.__name__
            # split cls_name by capital letters
            cls_name = ''.join([' ' + i.lower() if i.isupper() else i for i in cls_name]).strip()
            return cls_name + cls.description 

        # Get the description parameter for each class
        tools = []
        for cls in classes_tools:
            if issubclass(cls, object) and cls is not object:
                desc_for_search = tool_summary(cls)
                tools.append({
                    'name': cls.__name__,
                    'description': cls.description,
                    'input_parameters': cls.input_parameters,
                    'output_parameters': cls.output_parameters,
                    'desc_for_search': desc_for_search
                })

        self.tools = tools

    def search(self, keywords):
        # Searches for relevant tools in various libraries based on the keyword.
        input_parameters = {
            'keywords': keywords
        }
        try:
            best_match = self.best_match_api(keywords)
        except Exception as e:
            exception = str(e)
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': None, 'exception': exception}
        else:
            return {'api_name': self.__class__.__name__, 'input': input_parameters, 'output': best_match, 'exception': None}

    # use cosine similarity to find the best match
    def best_match_api(self, keywords):
        model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L3-v2')
        kw_emb = model.encode(keywords)
        best_match = None
        best_match_score = 0
        for api in self.tools:
            re_emb = model.encode(api['desc_for_search'])
            cos_sim = util.cos_sim(kw_emb, re_emb).item()
            if cos_sim > best_match_score:
                best_match = api.copy()
                best_match_score = cos_sim
        best_match.pop('desc_for_search')
        return best_match
    
    # create a plot with the embeddings of the tools
    def plot_embeddings(self):
        model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L3-v2')
        tool_embeddings = model.encode([tool['desc_for_search'] for tool in self.tools])
        # plot points in 2D
        import matplotlib.pyplot as plt
        from sklearn.decomposition import PCA
        import numpy as np
        pca = PCA(n_components=2)
        pca.fit(tool_embeddings)
        tool_embeddings_2d = pca.transform(tool_embeddings)
        plt.scatter(tool_embeddings_2d[:,0], tool_embeddings_2d[:,1])
        for i, tool in enumerate(self.tools):
            plt.annotate(tool['name'], (tool_embeddings_2d[i,0], tool_embeddings_2d[i,1]))
        plt.show()



class ToolsManager:

    def __init__(self):
        tools_dir = ('./tools')
        classes_tools = []
        except_files = ['__init__.py', '__pycache__']
        for file in os.listdir(tools_dir):
            if file.endswith('.py') and file not in except_files:
                api_file = file.split('.')[0]
                basename = os.path.basename(tools_dir)
                module = importlib.import_module(f'{basename}.{api_file}')
                classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
                for cls in classes:
                    classes_tools.append(cls)

        tools = []
        for cls in classes_tools:
            name = cls.__name__
            cls_info = {
                'name': name,
                'class': cls,
                'description': cls.description,
                'input_parameters': cls.input_parameters,
                'output_parameters': cls.output_parameters,
            }
            tools.append(cls_info)

        self.tools = tools

        self.tool_searcher = ToolSearcher()

    def get_tool_by_name(self, name: str):
        for tool in self.tools:
            if tool['name'] == name:
                return tool
        raise Exception(f'No tool with name {name}')
    
    def get_tool_description(self, name: str):
        tool_info = self.get_tool_by_name(name).copy()
        tool_info.pop('class')
        return json.dumps(tool_info['description'])
    
    def tool_call(self, tool_name: str, **kwargs):
        # TODO: check if kwargs are correct
        tool_class = self.get_tool_by_name(tool_name)["class"]
        tool = tool_class()
        return tool.call(**kwargs)
    
    def command_line(self):
        mode = 'qa'
        if mode == 'qa':
            while True:
                tool_keywords = input('Please enter the KEYWORDS for the tool you want to use (\'exit\' to exit):\n')
                response = self.tool_searcher.search(tool_keywords)
                #tool = self.init_tool(response['output']['name'])
                print('The tool you want to use is: \n' + response['output']['name'])
                while True:
                    command = input('Please enter the PARAMETERS for the tool you want to use (\'exit\' to exit): \n')
                    if command == 'exit':
                        break
                    else:
                        command = command.replace(' ', '')
                        processed_parameters = command.split(',')
                        print(f"tool: {response['output']['name']} with ({processed_parameters})")
        elif mode == 'function_call':
            print("not implemented yet")
            while True:
                command = input('Please enter the command for the tool you want to use: \n')
                if command == 'exit':
                    break
                #api_name, param_dict = parse_api_call(command)
                #print(self.api_call(api_name, **param_dict))



if __name__ == '__main__':
    tools_manager = ToolsManager()
    tools_manager.tool_searcher.plot_embeddings()
    tools_manager.command_line()