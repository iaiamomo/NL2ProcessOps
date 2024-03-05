from tools.camera import CaptureImage
from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

def calibrate_cardboard_production():
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
        
        # If the speed was successfully set, end the process
        if speed_set:
            break
        else:
            # Handle the case where setting the speed fails, for robustness
            print("Failed to set the speed of the die cutting machine. Retrying...")
            continue

    return "Calibration process completed successfully."

if __name__ == "__main__":
    result = calibrate_cardboard_production()
    print(result)