import numpy as np

# Assuming the tools are already imported and available for use
# from tools import CaptureImage, CheckMarkers, SetSpeedDieMachine

def calibration_process():
    while True:
        # Capture a photo of the cardboard
        captured_image = CaptureImage.call()
        
        # Analyze the photo to check if all markers identified are ok
        markers_ok = CheckMarkers.call(image=captured_image)
        
        # If markers are not ok, the calibration process continues (loop)
        if not markers_ok:
            continue
        
        # If markers are ok, set the speed of the die cutting machine to 10000 RPM and end the process
        speed_set = SetSpeedDieMachine.call(speed=10000)
        if speed_set:
            print("Speed set to 10000 RPM. Calibration process completed.")
            break
        else:
            print("Failed to set speed. Exiting process.")
            break

if __name__ == "__main__":
    calibration_process()