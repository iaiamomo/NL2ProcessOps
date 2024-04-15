import threading

class TurnOn:
    description = {
        "name": "TurnOn",
        "description": "Turn on the 3D printer.",
        "more details": "It takes no input. It does not return anything.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "printer_3d"
    }

    def call():
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class HeatUpBedExtruder:
    description = {
        "name": "HeatUpBedExtruder",
        "description": "Heat up the bed and the extruder.",
        "more details": "It takes no input. It does not return anything.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "printer_3d"
    }

    def call():
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class Print:
    description = {
        "name": "Print",
        "description": "Print the object.",
        "more details": "It takes the object as input. It does not return anything.",
        "input_parameters": ["GCodeFile:str"],
        "output_parameters": [],
        "actor": "printer_3d"
    }

    def call(GCodeFile : str):
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return