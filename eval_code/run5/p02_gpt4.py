from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

class StoreCardboardRoll:
    @staticmethod
    def call(location: str):
        pass

class CheckMarkers:
    @staticmethod
    def call(image: np.matrix) -> bool:
        return True  # Placeholder return value

class SetSpeedDieMachine:
    @staticmethod
    def call(speed: int) -> bool:
        return True  # Placeholder return value

def calibrate_cardboard_production(image: np.matrix):
    # Continuously check markers on the cardboard
    while True:
        markers_ok = CheckMarkers.call(image)
        if markers_ok:
            break  # Exit the loop if markers are ok
    
    # Set the speed of the die cutting machine to 10000 RPM
    speed_set = SetSpeedDieMachine.call(10000)
    return speed_set

if __name__ == "__main__":
    # Example usage
    # Assuming an image of a cardboard is represented as a numpy matrix
    example_image = np.matrix([[0, 1], [1, 0]])  # Placeholder for an actual image
    calibration_success = calibrate_cardboard_production(example_image)
    print(f"Calibration successful: {calibration_success}")