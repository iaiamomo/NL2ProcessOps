import random

class AssembleParts:
    description = {
        "description": "Worker assembles parts.",
        "more details": "It takes no input. It returns no output.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "worker"
    }

    def call():
        return

class CheckTypeCardboard:
    description = {
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

class InsertCardboardTypeInfo:
    description = {
        "description": "Worker inserts the type of cardboard in the system.",
        "more details": "It takes the type of cardboard as input. It returns no output.",
        "input_parameters": ["type_cardboard:str"],
        "output_parameters": [],
        "actor": "worker"
    }

    def call(type_cardboard : str):
        return

class StoreCardboardRoll:
    description = {
        "description": "Worker stores the cardboard roll in the warehouse.",
        "more details": "It takes as input the location. It returns no output.",
        "input_parameters": ["location:str"],
        "output_parameters": [],
        "actor": "worker"
    }

    def call(location : str):
        return

