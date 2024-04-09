import numpy as np
def calibration_process():
    while True:
        captured_image = CaptureImage.call()
        markers_ok = CheckMarkers.call(image=captured_image)
        if check(not markers_ok):
            continue
        speed_set = SetSpeedDieMachine.call(speed=10000)
        if check(speed_set):
            print("Speed set to 10000 RPM. Calibration process completed.")
            break
        else:
            print("Failed to set speed. Exiting process.")
            break
if __name__ == "__main__":
    calibration_process()