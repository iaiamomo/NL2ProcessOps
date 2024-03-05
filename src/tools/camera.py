import numpy as np

class CaptureImage:
    description = {
        "description": "Capture of a photo of the cardboard from the camera.",
        "more details": "This tool takes no input and returns an image captured from the the camera. The image is returned as a numpy matrix.",
        "input_parameters": [],
        "output_parameters": ['image:np.matrix'],
        "actor": "camera"
    }

    def call() -> np.matrix:
        image = np.matrix([[1, 2], [3, 4]])
        return image
