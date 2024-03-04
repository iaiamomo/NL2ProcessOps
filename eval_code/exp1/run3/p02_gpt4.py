from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

def capture_photo_of_cardboard():
    # This function simulates capturing a photo of the cardboard.
    # In a real scenario, this would interface with a camera system.
    # Here, we return a simulated image as a numpy matrix.
    return np.random.rand(10, 10)  # Simulated image

def calibration_process():
    while True:
        # Capture photo of cardboard
        cardboard_image = capture_photo_of_cardboard()
        
        # Analyze photo
        markers_ok = CheckMarkers.call(image=cardboard_image)
        
        # Check if markers are ok
        if markers_ok:
            # Set machine speed to 10000 RPM
            speed_set = SetSpeedDieMachine.call(speed=10000)
            if speed_set:
                print("Machine speed set to 10000 RPM successfully.")
            else:
                print("Failed to set machine speed.")
            break  # End the process
        else:
            print("Markers not ok, capturing another photo.")

if __name__ == "__main__":
    calibration_process()