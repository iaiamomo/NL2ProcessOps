import threading

class ConfigureAssemblyLine:
    description = {
        "name": "ConfigureAssemblyLine",
        "description": "Configure the assembly line.",
        "more details": "This tool takes no input and does not return anything.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "assembly_line"
    }

    def call():
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return