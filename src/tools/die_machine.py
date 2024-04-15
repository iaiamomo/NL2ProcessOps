import threading

class SetSpeedDieMachine:
    description = {
        "name": "SetSpeedDieMachine",
        "description": "set the speed of the die cutting machine.",
        "more details": "It takes as input the speed. It returns a boolean value, True if the speed has been set, False otherwise.",
        "input_parameters": ["speed:int"],
        "output_parameters": ['speed_set:bool'],
        "actor": "die_machine"
    }

    def call(speed : int) -> bool:
        speed_set = True
        return speed_set
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return
