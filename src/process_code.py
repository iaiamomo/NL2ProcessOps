from tools.CaptureImage import CaptureImage
from tools.CheckMarkers import CheckMarkers
from tools.SetSpeed import SetSpeed

import numpy as np

def calibration_process():
    # Capture image
    image = CaptureImage.call()
    
    # Check markers
    markers_ok = CheckMarkers.call(image=image)
    
    if markers_ok:
        # Set speed
        speed_set = SetSpeed.call(speed=10000)
    
calibration_process()