from langchain.tools import tool
import numpy as np


@tool
def generate_image(content: str) -> str:
    """Generate an image from a string of text represeting the content of the image and returns the path."""
    return f"path of the generated image"

@tool
def capture_image() -> str:
    """Capture an image from the camera and returns the path."""
    return f"path of the captured image"

@tool
def count_trees(image_path: str) -> int:
    """Count the number of trees in an image and returns that number."""
    return np.random.randint(0, 10)

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def move_the_robot(x: int, y: int) -> str:
    """Moves the robot to the specified coordinates."""
    return f"Robot moved to ({x}, {y})"

class ToolRepo():

    def __init__(self) -> None:
        pass

    def get_tools(self):
        self.tools = [
            generate_image,
            capture_image,
            count_trees,
            get_word_length,
            move_the_robot,
        ]
        return self.tools


if __name__ == "__main__":
    tool_repo = ToolRepo()
    tools = tool_repo.get_tools()
    for tool in tools:
        print(tool.name)
        print(tool.description)
        print(tool.function)