import threading

class L12SetUp:
    description = {
        "name": "L12SetUp",
        "description": "Set up the L12 line for spindle assembly.",
        "more details": "This tool takes no input and returns a boolean indicating if the line has been set up.",
        "input_parameters": [],
        "output_parameters": ['set_up:bool'],
        "actor": "l12"
    }

    def call() -> bool:
        set_up = True
        return set_up
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return


class L12AssembleSpindle:
    description = {
        "name": "L12AssembleSpindle",
        "description": "Assembly of a spindle over the L12 line.",
        "more details": "This tool takes as input the part list of a spindle. It returns a boolean indicating if the spindle has been assembled.",
        "input_parameters": ['part_list:list'],
        "output_parameters": ['assembled:bool'],
        "actor": "l12"
    }

    def call(part_list: list) -> bool:
        assembled = True
        return assembled
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return