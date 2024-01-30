import numpy as np

class RetrievePartList:
    description = {
        "description": """
        The warehouse system retrieves all parts of a part list of a product.
        This tool takes as input the part list of a product.
        It returns a boolean indicating if all the parts are retrieved.
        """,
        "input_parameters": {
            'part_list': {'type': 'list', 'description': 'list of parts of a product'}
        },
        "output_parameters": {
            "retrieved": {"type": "boolean", "description": "boolean indicating if all the parts are retrieved"}
        },
        "actor": "wms_is"
    }

    def call(part_list: list) -> bool:
        retrieved = np.random.choice([True, False])
        return retrieved