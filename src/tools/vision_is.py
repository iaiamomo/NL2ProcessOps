import numpy as np
import threading

class CheckMarkers:
    description = {
        "name": "CheckMarkers",
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
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class CountTrees:
    description = {
        "name": "CountTrees",
        "description": "Count the number of trees in an image",
        "more details": "It takes as input an image as a numpy matrix. It returns the number of trees in the image.",
        "input_parameters": ["image:np.matrix"],
        "output_parameters": ["number_of_trees:int"],
        "actor": "vision_is"
    }

    def call(image: np.matrix) -> bool:
        number_of_trees = 5
        return number_of_trees

    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class CheckQualityBrackets:
    description = {
        "name": "CheckQualityBrackets",
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
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class AnalyzeWarehouse:
    description = {
        "name": "AnalyzeWarehouse",
        "description": "Identify where to store a new cardboard roll.",
        "more details": "It takes as input an image of the warehouse and the type of cardboard roll. It returns the location where to store the new product.",
        "input_parameters": ["image:np.matrix", "type_cardboard:str"],
        "output_parameters": ["location:str"],
        "actor": "vision_is"
    }

    def call(image: np.matrix, type_cardboard: str) -> str:
        location = "A1"
        return location
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return