from vision_is import CheckMarkers
from die_machine import SetSpeedDieMachine

def calibration_process():
    while True:
        # Capture a photo of the cardboard
        image = capture_photo()  # This function needs to be implemented

        # Analyze the photo to check if all the markers are ok
        markers_ok = CheckMarkers.call(image)

        if markers_ok:
            # If the markers are ok, set the speed of the die cutting machine to 10000 RPM
            SetSpeedDieMachine.call(10000)
            break