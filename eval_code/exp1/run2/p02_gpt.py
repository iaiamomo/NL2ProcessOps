from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

def capture_photo_of_cardboard():
    # Simulate capturing a photo. In a real scenario, this would interface with a camera.
    # Here, we just return a placeholder numpy matrix representing an image.
    return np.matrix([[1, 0, 1], [0, 1, 0], [1, 0, 1]])

def calibration_process():
    while True:
        # Capture photo of cardboard
        cardboard_image = capture_photo_of_cardboard()
        
        # Analyze photo
        markers_ok = CheckMarkers.call(image=cardboard_image)
        
        # Check if markers are ok
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