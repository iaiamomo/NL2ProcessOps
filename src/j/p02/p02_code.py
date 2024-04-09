import numpy as np

def calibrate_cardboard_production():
    while True:
        captured_image = CaptureImage.call()
        markers_ok = CheckMarkers.call(image=captured_image)
        if markers_ok:
            speed_set = SetSpeedDieMachine.call(speed=10000)
            if speed_set:
                return "Calibration successful and speed set to 10000 RPM."
            else:
                return "Failed to set speed to 10000 RPM."
        # If markers are not ok, the loop continues to capture and analyze the next photo

if __name__ == "__main__":
    result = calibrate_cardboard_production()
    print(result)