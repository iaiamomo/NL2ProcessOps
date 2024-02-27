from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

def capture_photo():
    # Simulate capturing a photo of the cardboard
    # This is a placeholder for the actual photo capturing logic
    # For simplicity, we return a numpy matrix representing the photo
    return np.random.rand(10, 10)  # Random photo for demonstration

def calibration_process():
    while True:
        photo = capture_photo()
        markers_ok = CheckMarkers.call(image=photo)
        if markers_ok:
            speed_set = SetSpeedDieMachine.call(speed=10000)
            if speed_set:
                print("Calibration process completed successfully.")
                break
            else:
                print("Failed to set the speed of the die cutting machine.")
        else:
            print("Markers not OK. Repeating the calibration process.")

if __name__ == "__main__":
    calibration_process()