import numpy as np

class GenerateImage:
    description = {
        "description": """
        Useful for generating images from a text content.
        This tool takes as input a text content and returns an image as a numpy matrix.
        """,
        "input_parameters": {
            'content': {'type': 'str', 'description': 'content of the image'}
        },
        "output_parameters": {
            'image': {'type': 'np.matrix', 'description': 'image generated from the text content'}
        },
    }


    def call(content : str) -> np.matrix:
        image = np.matrix([[1, 2], [3, 4]])
        return image