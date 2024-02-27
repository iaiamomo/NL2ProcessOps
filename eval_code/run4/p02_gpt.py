from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

# Assuming the CheckMarkers and SetSpeedDieMachine tools are already imported

def capture_photo_of_cardboard():
    """
    Simulates capturing a photo of the cardboard.
    This is a placeholder function to simulate the action of capturing a photo.
    In a real scenario, this function would interface with a camera device.
    
    Returns:
        np.matrix: A simulated image of a cardboard.
    """
    # Simulate an image capture of the cardboard
    # This is a placeholder. In a real scenario, actual image data would be returned.
    return np.matrix([[1, 0, 1], [0, 1, 0], [1, 0, 1]])

def calibration_process():
    """
    Executes the calibration process of a cardboard production.
    """
    while True:
        # Capture photo of cardboard
        cardboard_image = capture_photo_of_cardboard()
        
        # Analyze photo
        markers_ok = CheckMarkers.call(image=cardboard_image)
        
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