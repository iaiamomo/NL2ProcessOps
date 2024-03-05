from tools.camera import CaptureImage
from tools.worker import StoreCardboardRoll
from tools.worker import CheckTypeCardboard
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

def calibration_process():
    while True:
        # Capture photo of cardboard
        captured_image = CaptureImage.call()
        
        # Analyze photo
        markers_ok = CheckMarkers.call(image=captured_image)
        
        # Exclusive gateway to check if markers are ok
        if markers_ok:
            # Set speed of die cutting machine to 10000 RPM
            speed_set = SetSpeedDieMachine.call(speed=10000)
            if speed_set:
                print("Die cutting machine speed set to 10000 RPM successfully.")
            else:
                print("Failed to set die cutting machine speed.")
            break
        else:
            print("Markers not ok, capturing another photo.")

if __name__ == "__main__":
    calibration_process()