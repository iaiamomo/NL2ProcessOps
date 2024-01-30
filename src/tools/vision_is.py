import numpy as np

class CheckMarkers:
    description = {
        "description": """
        The vision system checks if markers are present on the cardboard.
        This tool takes as input an image depicting a cardboard.
        It returns a boolean indicating if markers are present on the cardboard.
        """,
        "input_parameters": {
            'image': {'type': 'np.matrix', 'description': 'image depicting a cardboard'}
        },
        "output_parameters": {
            "markers_ok": {"type": "bool", "description": "boolean indicating if markers are present on the cardboard"}
        },
        "actor": "vision_is"
    }

    def call(image: np.matrix) -> bool:
        #randomly return True or False
        markers_ok = np.random.choice([True, False])
        return markers_ok


class CountTrees:
    description = {
        "description": """
        The vision system counts the number of trees in an image.
        It takes as input an image as a numpy matrix.
        It returns the number of trees in the image.
        """,
        "input_parameters": {
            'image': {'type': 'np.matrix', 'description': 'image'}
        },
        "output_parameters": {
            "number_of_trees": {"type": "int", "description": "number of trees in the image"}
        },
        "file": "vision_is"
    }

    def call(image: np.matrix) -> bool:
        number_of_trees = 5
        return number_of_trees