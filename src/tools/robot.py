import threading

class MoveRobot:
    description = {
        "name": "MoveRobot",
        "description": "Move the robot.",
        "more details": "It takes as input the coordinates of the destination. It return a boolean value, True if the robot has reached the destination, False otherwise.",
        "input_parameters": ["x:int", "y:int"],
        "output_parameters": ['destination_reached:bool'],
        "actor": "robot"
    }

    def call(x : int, y : int) -> bool:
        destination_reached = True
        return destination_reached
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return
