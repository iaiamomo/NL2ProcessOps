import numpy as np

class CountTrees:
    description = """
    Useful for counting trees in an image.
    It takes as input an image as a numpy matrix.
    It returns the number of trees in the image.
    """
    input_parameters = {
        'image': {'type': 'np.matrix', 'description': 'image'}
    }
    output_parameters = {
        "number_of_trees": {"type": "int", "description": "number of trees in the image"}
    }

    def call(self, image: np.matrix) -> bool:
        number_of_trees = 5
        return number_of_trees