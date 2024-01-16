from sentence_transformers import SentenceTransformer, util
import logging
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
import os

class ToolSearcher():

    def __init__(self):
        import importlib.util

        tools_dir = ('./tools')
        classes = []
        except_files = ['__init__.py', '__pycache__']
        for file in os.listdir(tools_dir):
            if file.endswith('.py') and file not in except_files:
                api_file = file.split('.')[0]
                basename = os.path.basename(tools_dir)
                module = importlib.import_module(f'{basename}.{api_file}')
                classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
                for cls in classes:
                    classes.append(cls)

        def tool_summary(cls):
            cls_name = cls.__name__
            # split cls_name by capital letters
            cls_name = ''.join([' ' + i.lower() if i.isupper() else i for i in cls_name]).strip()
            return cls_name + cls.description 

        # Get the description parameter for each class
        tools = []
        for cls in classes:
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
        """
        Searches for relevant tools in various libraries based on the keyword.

        Parameters:
        - keywords (str): the keywords to search for.

        Returns:
        - best_match (dict): the best match for the keywords.
        """
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

    def best_match_api(self, keywords):
        model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L3-v2')
        kw_emb = model.encode(keywords)
        best_match = None
        best_match_score = 0
        for api in self.apis:
            re_emb = model.encode(api['desc_for_search'])
            cos_sim = util.cos_sim(kw_emb, re_emb).item()
            if cos_sim > best_match_score:
                best_match = api.copy()
                best_match_score = cos_sim
        best_match.pop('desc_for_search')
        if 'token' in best_match['input_parameters']:
            return [self.get_user_token_api, best_match]
        else:
            return best_match