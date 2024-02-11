import numpy as np

class RetrievePartList:
    description = {
        "description": "Retrieve raw materials.",
        "more details": "This tool takes as input the part list of a product. It returns a boolean indicating if all the parts are retrieved.",
        "input_parameters": ["part_list:list"],
        "output_parameters": ["retrieved:bool"],
        "actor": "wms_is"
    }

    def call(part_list: list) -> bool:
        retrieved = np.random.choice([True, False])
        return retrieved