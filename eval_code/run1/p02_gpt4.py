from tools.camera import CaptureImage
from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

# Assuming the tools are already imported and available for use
# from tools import CaptureImage, CheckMarkers, SetSpeedDieMachine

def calibration_process():
    while True:
        # Capture photo of the cardboard
        captured_image = CaptureImage.call()
        
        # Analyze photo to check if all markers identified are ok
        markers_ok = CheckMarkers.call(image=captured_image)
        
        # If markers are not ok, the calibration process continues (loop)
        if not markers_ok:
            continue
        
        # If markers are ok, set the speed of the die cutting machine to 10000 RPM and end the process
        speed_set = SetSpeedDieMachine.call(speed=10000)
        if speed_set:
            print("Machine speed set to 10000 RPM successfully.")
        else:
            print("Failed to set machine speed.")
        break

if __name__ == "__main__":
    calibration_process()