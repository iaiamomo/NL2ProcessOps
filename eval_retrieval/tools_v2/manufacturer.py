import random

class SendSketches:
    description = {
        "description": "Send the sketches of the project to the artist.",
        "more details": "It takes no input. It returns the description of the project.",
        "input_parameters": [],
        "output_parameters": ["project:str"],
        "actor": "manufacturer"
    }

    def call() -> str:
        project = "The project is to create a new product."
        return project

class ChoosePlasticColor:
    description = {
        "description": "Choose the color of the plastic.",
        "more details": "It takes no input. It returns the color of the plastic.",
        "input_parameters": [],
        "output_parameters": ["color:int"],
        "actor": "manufacturer"
    }

    def call() -> int:
        # random rgb color
        color = random.randint(0, 0xFFFFFF)
        return color

class CheckColorAvailability:
    description = {
        "description": "Check the availability of the color.",
        "more details": "It takes the color as input. It returns the availability of the color.",
        "input_parameters": ["color:int"],
        "output_parameters": ["availability:bool"],
        "actor": "manufacturer"
    }

    def call(color : int) -> bool:
        availability = random.choice([True, False])
        return availability

class OrderColor:
    description = {
        "description": "Order the color.",
        "more details": "It takes the color as input. It does not return anything.",
        "input_parameters": ["color:int"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(color : int):
        return

class CheckColorQuantity:
    description = {
        "description": "Check the quantity of the color.",
        "more details": "It takes the color as input. It returns the quantity of the color in grams.",
        "input_parameters": ["color:int"],
        "output_parameters": ["quantity:int"],
        "actor": "manufacturer"
    }

    def call(color : int) -> int:
        quantity = random.randint(0, 100)
        return quantity

class UpdateShoppingList:
    description = {
        "description": "Update the shopping list.",
        "more details": "It takes the color type as input. It does not return anything.",
        "input_parameters": ["color:int"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(color : int):
        shopping_list = f"{color}"
        return

class GenerateGCode:
    description = {
        "description": "Generate the GCode file for the printer.",
        "more details": "It takes the object as input. It returns the GCode file.",
        "input_parameters": ["project:str"],
        "output_parameters": ["gcode:str"],
        "actor": "manufacturer"
    }

    def call(project : str) -> str:
        gcode = "GCode"
        return gcode

class SendRequirements:
    description = {
        "description": "Send the requirements (part list) to the proper teams.",
        "more details": "It takes the list of requirements. It does not return anything.",
        "input_parameters": ["part_list:list"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(part_list : list):
        return

class ReceiveParts:
    description = {
        "description": "Receive the individual parts from the teams.",
        "more details": "It takes no input. It does not return anything.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call():
        return

class AssembleInterior:
    description = {
        "description": "Assemble the interior of the plane.",
        "more details": "It takes the part list and the plane id. It does not return anything.",
        "input_parameters": ["part_list:list", "product_id:int"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(part_list : list, product_id : int):
        return

class CreateTestProtocol:
    description = {
        "description": "Create the test protocol for the product.",
        "more details": "It takes the part list and the product id. It returns the test protocol.",
        "input_parameters": ["part_list:list", "product_id:int"],
        "output_parameters": ["test_protocol:str"],
        "actor": "manufacturer"
    }

    def call(part_list : list, product_id : int) -> str:
        test_protocol = "Test protocol"
        return test_protocol

class GenerateRequirementTreeHouse:
    description = {
        "description": "Generate the requirement for the tree house.",
        "more details": "It takes no input. It returns the part list.",
        "input_parameters": [],
        "output_parameters": ["part_list:list"],
        "actor": "manufacturer"
    }

    def call() -> list:
        part_list = ["wood", "nails", "screws", "plastic"]
        return part_list

class SendRequirementsArchitect:
    description = {
        "description": "Send the requirements to the architect.",
        "more details": "It takes the part list. It does not return anything.",
        "input_parameters": ["part_list:list"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(part_list : list):
        
        return

class RefineRequirementsTreeHouse:
    description = {
        "description": "Refine the requirements for the tree house.",
        "more details": "It takes the part list. It returns the refined part list.",
        "input_parameters": ["part_list:list"],
        "output_parameters": ["refined_part_list:list"],
        "actor": "manufacturer"
    }

    def call(part_list : list) -> list:
        refined_part_list = part_list
        return refined_part_list

class OrderParts:
    description = {
        "description": "Manufacturer orders the parts online.",
        "more details": "It takes the part list. It does not return anything.",
        "input_parameters": ["part_list:list"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(part_list : list):
        return

class SendMessage:
    description = {
        "description": "Send a message to people.",
        "more details": "It takes the message. It does not return anything.",
        "input_parameters": ["message:str"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(message : str):
        return

class AssembleTreeHouse:
    description = {
        "description": "Assemble the tree house.",
        "more details": "It takes the part list. It does not return anything.",
        "input_parameters": ["part_list:list"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(part_list : list):
        return

class CreateListOfPeople:
    description = {
        "description": "Create the list of people to invite.",
        "more details": "It takes no input. It returns the list of people.",
        "input_parameters": [],
        "output_parameters": ["people:list"],
        "actor": "manufacturer"
    }

    def call() -> list:
        people = ["Alice", "Bob", "Charlie"]
        return people

class SendInvitations:
    description = {
        "description": "Send the invitations to the people.",
        "more details": "It takes the list of people. It does not return anything.",
        "input_parameters": ["people:list"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(people : list):
        return

class BuySnacks:
    description = {
        "description": "Buy snacks for the party.",
        "more details": "It takes the list of people. It does not return anything.",
        "input_parameters": ["people:list"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(people : list):
        return

class AssembleBicycle:
    description = {
        "description": "Assemble the bicycle.",
        "more details": "It takes the part list. It does not return anything.",
        "input_parameters": ["part_list:list"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(part_list : list):
        return

class InformStorehouseEngineering:
    description = {
        "description": "Inform the storehouse and the engineering departments.",
        "more details": "It takes the part list and the product id. It does not return anything.",
        "input_parameters": ["part_list:list", "product_id:int"],
        "output_parameters": [],
        "actor": "manufacturer"
    }

    def call(part_list : list, product_id : int):
        return