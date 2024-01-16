from langchain.tools import tool
import numpy as np


@tool
def capture_image() -> str:
    """Capture an image from a camera and returns the path of the image."""
    return f"path_to_image_{np.random.randint(0, 100)}.png"

@tool
def check_marker(image_path: str, idx_marker: int) -> bool:
    """Check if marker idx on the cardboard is ok. If it is ok, return True, otherwise False."""
    return True

@tool
def count_markers(image_path: str) -> int:
    """Count the markers on the cardboard and return the number of markers."""
    return np.random.randint(0, 10)

@tool
def check_colors(image_path: str) -> bool:
    """Check if the colors of the printed cardboard are ok."""
    return True

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def move_the_robot(x: int, y: int) -> str:
    """Moves the robot to the specified coordinates."""
    return f"Robot moved to ({x}, {y})"

class ToolRepo():
    def get_tools(self):
        self.tools = [
            capture_image,
            count_markers,
            check_marker,
            check_colors,
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