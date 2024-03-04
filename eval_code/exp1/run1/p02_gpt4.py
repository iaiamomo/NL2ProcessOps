from tools.camera import CaptureImage
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

def calibration_process():
    while True:
        photo = CaptureImage.call()
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