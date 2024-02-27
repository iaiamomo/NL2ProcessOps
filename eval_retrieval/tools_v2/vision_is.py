import numpy as np

class CheckMarkers:
    description = {
        "description": "Analysis of the markers on a cardboard image.",
        "more details": "This tool takes as input an image depicting a cardboard. It returns a boolean indicating if markers are present on the cardboard.",
        "input_parameters": ["image:np.matrix"],
        "output_parameters": ["markers_ok:bool"],
        "actor": "vision_is"
    }

    def call(image: np.matrix) -> bool:
        #randomly return True or False
        markers_ok = np.random.choice([True, False])
        return markers_ok

class CountTrees:
    description = {
        "description": "Count the number of trees in an image",
        "more details": "It takes as input an image as a numpy matrix. It returns the number of trees in the image.",
        "input_parameters": ["image:np.matrix"],
        "output_parameters": ["number_of_trees:int"],
        "actor": "vision_is"
    }

    def call(image: np.matrix) -> bool:
        number_of_trees = 5
        return number_of_trees

class CheckQualityBrackets:
    description = {
        "description": "Check the quality of the brackets.",
        "more details": "It takes no input. It returns a boolean indicating if the brackets are of good quality.",
        "input_parameters": [],
        "output_parameters": ["quality_ok:bool"],
        "actor": "vision_is"
    }

    def call(image: np.matrix) -> bool:
        #randomly return True or False
        quality_ok = np.random.choice([True, False])
        return quality_ok

class AnalyzeWarehouse:
    description = {
        "description": "Identify where to store a new cardboard roll.",
        "more details": "It takes as input an image of the warehouse and the type of cardboard roll. It returns the location where to store the new product.",
        "input_parameters": ["image:np.matrix", "type_cardboard:str"],
        "output_parameters": ["location:str"],
        "actor": "vision_is"
    }

    def call(image: np.matrix, type_cardboard: str) -> str:
        location = "A1"
        return location