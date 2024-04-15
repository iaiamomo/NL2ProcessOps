import threading

class AssembleParts:
    description = {
        "name": "AssembleParts",
        "description": "The welding machine assemble the parts into brackets.",
        "more details": "This tool takes no input and does not return anything.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "welding_machine"
    }

    def call():
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return