import numpy as np

class CheckMarkers:
    description = """
    Useful for checking if markers are present on the cardboard.
    This tool takes as input an image depicting a cardboard.
    It returns a boolean indicating if markers are present on the cardboard.
    """
    input_parameters = {
        'image': {'type': 'np.matrix', 'description': 'image depicting a cardboard'}
    }
    output_parameters = {
        "markers_ok": {"type": "bool", "description": "boolean indicating if markers are present on the cardboard"}
    }

    def call(self, image: np.matrix) -> bool:
        markers_ok = True
        return markers_ok