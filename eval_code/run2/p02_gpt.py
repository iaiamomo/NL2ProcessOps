from tools.worker import StoreCardboardRoll
from tools.worker import CheckTypeCardboard
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

class CapturePhoto:
    @staticmethod
    def call():
        # Simulate capturing a photo of the cardboard
        # This is a placeholder for the actual implementation
        # Returns a simulated image as a numpy matrix
        return np.matrix([[1, 0], [0, 1]])

class CheckMarkers:
    @staticmethod
    def call(image: np.matrix) -> bool:
        # Placeholder for marker analysis
        # Returns True if markers are ok, False otherwise
        # This should be replaced with the actual implementation
        return True

class SetSpeedDieMachine:
    @staticmethod
    def call(speed: int) -> bool:
        # Placeholder for setting the speed of the die cutting machine
        # Returns True if the speed was successfully set, False otherwise
        # This should be replaced with the actual implementation
        return True

def calibration_process():
    while True:
        # Capture photo of the cardboard
        image = CapturePhoto.call()
        
        # Analyze photo
        markers_ok = CheckMarkers.call(image)
        
        # Check if markers are ok
        if markers_ok:
            # Set speed of die cutting machine to 10000 RPM
            speed_set = SetSpeedDieMachine.call(10000)
            if speed_set:
                print("Speed set successfully.")
            else:
                print("Failed to set speed.")
            break
        else:
            print("Markers not ok, capturing another photo.")

if __name__ == "__main__":
    calibration_process()