import numpy as np
import threading

class RetrieveRawMaterials:
    description = {
        "name": "RetrieveRawMaterials",
        "description": "Warehouse deparment evaluates part list and retrieve raw materials.",
        "more details": "This tool takes as input the part list of a product. It returns a boolean indicating if all the parts are retrieved.",
        "input_parameters": ["part_list:list"],
        "output_parameters": ["retrieved:bool"],
        "actor": "wms_is"
    }

    def call(part_list: list) -> bool:
        retrieved = np.random.choice([True, False])
        return retrieved
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class RetrieveRawMaterial:
    description = {
        "name": "RetrieveRawMaterial",
        "description": "Warehouse department retrieves a raw material.",
        "more details": "It takes the part as input. It returns a boolean indicating if the part is retrieved.",
        "input_parameters": ["part:str"],
        "output_parameters": ["retrieved:bool"],
        "actor": "wms_is"
    }

    def call(part: str) -> bool:
        retrieved = np.random.choice([True, False])
        return retrieved
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class OrderRawMaterial:
    description = {
        "name": "OrderRawMaterial",
        "description": "Warehouse deparment orders the raw material.",
        "more details": "It takes the part as input. It does not return anything.",
        "input_parameters": ["part:str"],
        "output_parameters": [],
        "actor": "wms_is"
    }

    def call(part: str):
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class UpdateStock:
    description = {
        "name": "UpdateStock",
        "description": "Warehouse department updates the stock of a product.",
        "more details": "It takes as input the product type. It does not return anything.",
        "input_parameters": ["product_type:str"],
        "output_parameters": [],
        "actor": "wms_is"
    }

    def call(product_type: str):
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return