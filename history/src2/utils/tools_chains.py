from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from typing import Optional
import json
import numpy as np

def getTools():
    tools = []
    tools.append(CaptureImage())
    tools.append(CheckMarkers())
    tools.append(CountTrees())
    tools.append(GenerateImage())
    tools.append(GetWordLength())
    tools.append(MoveRobot())
    return tools

class CaptureImage(BaseTool):
    name = "capture_image"
    description = json.dumps(
        {
            "name": "capture_image",
            "description": """
            Useful for capturing images from a camera.
            This tool takes no input and returns an image from the the camera.
            The image is returned as a numpy matrix.
            """,
            "input": [],
            "output": [{"name": "image", "type": "np.matrix"}],
        }, indent=4
    )

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> np.matrix:
        """Use the tool."""
        raise NotImplementedError("capture_image does not support sync")

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> np.matrix:
        """Use the tool asynchronously."""
        raise NotImplementedError("capture_image does not support async")

class CheckMarkers(BaseTool):
    name = "check_markers"
    description = json.dumps(
        {
            "name": "check_markers",
            "description": """
            Useful for checking if markers are present on the cardboard.
            This tool takes as input an image depicting a cardboard.
            It returns a boolean indicating if markers are present on the cardboard.
            """,
            "input": [{"name": "image", "type": "np.matrix"}],
            "output": [{"name": "markers_ok", "type": "bool"}],
        }, indent=4
    )

    def _run(
        self,
        image_path: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> bool:
        """Use the tool."""
        raise NotImplementedError("check_markers does not support sync")
    
    async def _arun(
        self,
        image_path: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """Use the tool asynchronously."""
        raise NotImplementedError("check_markers does not support async")

class CountTrees(BaseTool):
    name = "count_trees"
    description = json.dumps(
        {
            "name": "count_trees",
            "description": """
            Useful for counting trees in an image.
            It takes as input an image as a numpy matrix.
            It returns the number of trees in the image.
            """,
            "input": [{"name": "image", "type": "np.matrix"}],
            "output": [{"name": "number_of_trees", "type": "int"}],
        }, indent=4
    )

    def _run(
        self,
        image_path: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> int:
        """Use the tool."""
        raise NotImplementedError("count_trees does not support sync")
    
    async def _arun(
        self,
        image_path: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> int:
        """Use the tool asynchronously."""
        raise NotImplementedError("count_trees does not support async")

class GenerateImage(BaseTool):
    name = "generate_image"
    description = json.dumps(
        {
            "name": "generate_image",
            "description": """
            Useful for generating images from text.
            This tool takes as input a text and returns an image as a numpy matrix.
            """,
            "input": [{"name": "content", "type": "str"}],
            "output": [{"name": "image", "type": "np.matrix"}],
        }, indent=4
    )

    def _run(
        self,
        content: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> np.matrix:
        """Use the tool."""
        raise NotImplementedError("generate_image does not support sync")
    
    async def _arun(
        self,
        content: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> np.matrix:
        """Use the tool asynchronously."""
        raise NotImplementedError("generate_image does not support async")

class GetWordLength(BaseTool):
    name = "get_word_length"
    description = json.dumps(
        {
            "name": "get_word_length",
            "description": """
            Useful for computing the length of a word.
            It takes as input a word.
            It returns the length of the word.""",
            "input": [{"name": "word", "type": "str"}],
            "output": [{"name": "length", "type": "int"}],
        }, indent=4
    )

    def _run(
        self,
        word: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> int:
        """Use the tool."""
        raise NotImplementedError("get_word_length does not support sync")
    
    async def _arun(
        self,
        word: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> int:
        """Use the tool asynchronously."""
        raise NotImplementedError("get_word_length does not support async")

class MoveRobot(BaseTool):
    name = "move_robot"
    description = json.dumps(
        {
            "name": "move_robot",
            "description": """
            Useful for moving a robot inside a room.
            It takes as input the coordinates of the destination.
            It returns a boolean value, True if the robot has reached the destination, False otherwise.
            """,
            "input": [{"name": "x", "type": "int"}, {"name": "y", "type": "int"}],
            "output": [{"name": "destination_reached", "type": "bool"}],
        }, indent=4
    )

    def _run(
        self,
        x: int,
        y: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> bool:
        """Use the tool."""
        raise NotImplementedError("move_robot does not support sync")
    
    async def _arun(
        self,
        x: int,
        y: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """Use the tool asynchronously."""
        raise NotImplementedError("move_robot does not support async")