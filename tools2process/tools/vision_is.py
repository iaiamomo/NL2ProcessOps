import numpy as np

class CheckMarkers:
    description = {
        "description": "Analysis of the markers on a cardboard image",
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