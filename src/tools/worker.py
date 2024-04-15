import random
import threading

class AssembleParts:
    description = {
        "name": "AssembleParts",
        "description": "Worker assembles parts.",
        "more details": "It takes no input. It returns no output.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "worker"
    }

    def call():
        return

    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class CheckTypeCardboard:
    description = {
        "name": "CheckTypeCardboard",
        "description": "Worker checks the type of cardboard.",
        "more details": "It takes no input. It returns no output.",
        "input_parameters": [],
        "output_parameters": ["type_cardboard:str"],
        "actor": "worker"
    }

    def call() -> str:
        # random between brown and white
        type_cardboard = random.choice(["brown", "white"])
        return type_cardboard
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class InsertCardboardTypeInfo:
    description = {
        "name": "InsertCardboardTypeInfo",
        "description": "Worker inserts the type of cardboard in the system.",
        "more details": "It takes the type of cardboard as input. It returns no output.",
        "input_parameters": ["type_cardboard:str"],
        "output_parameters": [],
        "actor": "worker"
    }

    def call(type_cardboard : str):
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class StoreCardboardRoll:
    description = {
        "name": "StoreCardboardRoll",
        "description": "Worker stores the cardboard roll in the warehouse.",
        "more details": "It takes as input the location. It returns no output.",
        "input_parameters": ["location:str"],
        "output_parameters": [],
        "actor": "worker"
    }

    def call(location : str):
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

