from tools.camera import CaptureImage
from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine

import numpy as np

def calibration_process():
    while True:
        # Capture a photo of the cardboard
        image = CaptureImage.call()
        
        # Analyze the photo to check if all markers are ok
        markers_ok = CheckMarkers.call(image=image)
        
        # If markers are not ok, the calibration process continues (loop)
        if not markers_ok:
            continue
        
        # If markers are ok, set the speed of the die cutting machine to 10000 RPM
        speed_set = SetSpeedDieMachine.call(speed=10000)
        
        # Assuming the process requires confirmation that the speed was successfully set
        if speed_set:
            print("Die cutting machine speed set to 10000 RPM successfully.")
        else:
            print("Failed to set die cutting machine speed to 10000 RPM.")
        
        # End the process
        break

if __name__ == "__main__":
    calibration_process()