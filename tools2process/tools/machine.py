
class SetSpeedMachine:
    description = {
        "description": "Set the speed of the machine.",
        "more details": "It takes as input the speed. It returns a boolean value, True if the speed has been set, False otherwise.",
        "input_parameters": ["speed:int"],
        "output_parameters": ['speed_set:bool'],
        "actor": "machine"
    }

    def call(speed : int) -> bool:
        speed_set = True
        return speed_set
