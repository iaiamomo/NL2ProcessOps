
class TurnOn:
    description = {
        "description": "Turn on the 3D printer.",
        "more details": "It takes no input. It does not return anything.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "printer_3d"
    }

    def call():
        return

class HeatUpBedExtruder:
    description = {
        "description": "Heat up the bed and the extruder.",
        "more details": "It takes no input. It does not return anything.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "printer_3d"
    }

    def call():
        return

class Print:
    description = {
        "description": "Print the object.",
        "more details": "It takes the object as input. It does not return anything.",
        "input_parameters": ["GCodeFile:str"],
        "output_parameters": [],
        "actor": "printer_3d"
    }

    def call(GCodeFile : str):
        return