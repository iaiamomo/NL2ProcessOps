import numpy as np

class GenerateImage:
    description = {
        "description": "Generate an image from a text content",
        "more details": "This tool takes as input a text content and returns an image as a numpy matrix.",
        "input_parameters": ["content:str"],
        "output_parameters": ["image:np.matrix"],
        "actor": "generator_llm"
    }

    def call(content : str) -> np.matrix:
        image = np.matrix([[1, 2], [3, 4]])
        return image
