
class MoveRobot:
    description = {
        "description": """
        Useful for moving a robot inside a factory.
        It takes as input the coordinates of the destination.
        It return a boolean value, True if the robot has reached the destination, False otherwise.
        """,
        "input_parameters": {
            'x': {'type': 'int', 'description': 'x coordinate of the destination'},
            'y': {'type': 'int', 'description': 'y coordinate of the destination'}
        },
        "output_parameters": {
            'destination_reached': {'type': 'bool', 'description': 'True if the robot has reached the destination, False otherwise'}
        },
    }

    def call(x : int, y : int) -> bool:
        destination_reached = True
        return destination_reached