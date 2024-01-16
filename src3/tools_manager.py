import os
import json

class ToolManager:

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

        tools = []
        for cls in classes:
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
                tool_keywords = input('Please enter the keywords for the tool you want to use (\'exit\' to exit):\n')
                tool_searcher = self.init_tool('ToolSearcher')
                response = tool_searcher.call(tool_keywords)
                tool = self.init_tool(response['output']['name'])
                print('The tool you want to use is: \n' + self.get_api_description(response['output']['name']))
                while True:
                    command = input('Please enter the parameters for the tool you want to use (\'exit\' to exit): \n')
                    if command == 'exit':
                        break
                    else:
                        command = command.replace(' ', '')
                        processed_parameters = command.split(',')
                        print(tool.call(*processed_parameters))
        elif mode == 'function_call':
            print("not implemented yet")
            while True:
                command = input('Please enter the command for the tool you want to use: \n')
                if command == 'exit':
                    break
                #api_name, param_dict = parse_api_call(command)
                #print(self.api_call(api_name, **param_dict))

if __name__ == '__main__':
    tool_manager = ToolManager()
    tool_manager.command_line()