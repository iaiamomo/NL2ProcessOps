import numpy as np

class RetrieveRawMaterials:
    description = {
        "description": "Warehouse deparment evaluates part list and retrieve raw materials.",
        "more details": "This tool takes as input the part list of a product. It returns a boolean indicating if all the parts are retrieved.",
        "input_parameters": ["part_list:list"],
        "output_parameters": ["retrieved:bool"],
        "actor": "wms_is"
    }

    def call(part_list: list) -> bool:
        retrieved = np.random.choice([True, False])
        return retrieved

class RetrieveRawMaterial:
    description = {
        "description": "Warehouse department retrieves a raw material.",
        "more details": "It takes the part as input. It returns a boolean indicating if the part is retrieved.",
        "input_parameters": ["part:str"],
        "output_parameters": ["retrieved:bool"],
        "actor": "wms_is"
    }

    def call(part: str) -> bool:
        retrieved = np.random.choice([True, False])
        return retrieved

class OrderRawMaterial:
    description = {
        "description": "Warehouse deparment orders the raw material.",
        "more details": "It takes the part as input. It does not return anything.",
        "input_parameters": ["part:str"],
        "output_parameters": [],
        "actor": "wms_is"
    }

    def call(part: str):
        return

class UpdateStock:
    description = {
        "description": "Warehouse department updates the stock of a product.",
        "more details": "It takes as input the product type. It does not return anything.",
        "input_parameters": ["product_type:str"],
        "output_parameters": [],
        "actor": "wms_is"
    }

    def call(product_type: str):
        return