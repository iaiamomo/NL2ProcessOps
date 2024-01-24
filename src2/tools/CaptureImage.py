import numpy as np

class CaptureImage:
    description = {
        "description": """
        Useful for capturing images from a camera.
        This tool takes no input and returns an image from the the camera.
        The image is returned as a numpy matrix.
        """,
        "input_parameters": {},
        "output_parameters": {
            'image': {'type': 'np.matrix', 'description': 'image captured from the camera'}
        },
    }

    def call() -> np.matrix:
        image = np.matrix([[1, 2], [3, 4]])
        return image