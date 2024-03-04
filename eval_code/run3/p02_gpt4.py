from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

def capture_photo():
    # Simulate capturing a photo. In a real scenario, this would interface with a camera.
    # Here, we just return a placeholder numpy matrix representing an image.
    return np.random.rand(10, 10)  # Placeholder for an image of the cardboard

def calibration_process():
    while True:
        photo = capture_photo()
        markers_ok = CheckMarkers.call(image=photo)
        if markers_ok:
            speed_set = SetSpeedDieMachine.call(speed=10000)
            if speed_set:
                print("Speed set to 10000 RPM. Calibration process completed.")
            else:
                print("Failed to set speed. Please check the die cutting machine.")
            break
        else:
            print("Markers not ok. Repeating the calibration process.")

if __name__ == "__main__":
    calibration_process()