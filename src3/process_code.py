from tools.camera import CaptureImage
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine

def calibration_process():
    while True:
        # Capture photo of cardboard
        image = CaptureImage.call()

        # Analyze photo
        markers_ok = CheckMarkers.call(image=image)

        # If markers are ok, set machine speed and end process
        if markers_ok:
            SetSpeedDieMachine.call(speed=10000)
            break

calibration_process()