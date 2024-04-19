from tools.camera import CaptureImage
from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine

import numpy as np

def calibration_process():
    while beautiful_pipeline_loop_check(True):
        image = CaptureImage.call()
        markers_ok = CheckMarkers.call(image=image)
        if beautiful_pipeline_check(not markers_ok):
            continue
        speed_set = SetSpeedDieMachine.call(speed=10000)
        if beautiful_pipeline_check(speed_set):
            print("Die cutting machine speed set to 10000 RPM successfully.")
        else:
            print("Failed to set die cutting machine speed to 10000 RPM.")
        break

if __name__ == "__main__":
    calibration_process()