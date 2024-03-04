from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine
import numpy as np

def calibrate_cardboard_production(image: np.matrix):
    """
    Calibrates the cardboard production process by analyzing the cardboard image
    for markers and setting the die cutting machine speed accordingly.

    Parameters:
    - image: np.matrix, a photo of the cardboard being produced.

    Returns:
    - bool, True if calibration was successful and speed was set, False otherwise.
    """
    # Continuously check markers until they are ok
    while True:
        markers_ok = CheckMarkers.call(image=image)
        if markers_ok:
            break

    # If markers are ok, set the speed of the die cutting machine to 10000 RPM
    speed_set = SetSpeedDieMachine.call(speed=10000)
    return speed_set

if __name__ == "__main__":
    # Example usage
    # Assuming `example_image` is a np.matrix representing the cardboard image
    example_image = np.matrix([[0, 1], [1, 0]])  # Placeholder for an actual image
    calibration_successful = calibrate_cardboard_production(example_image)
    print(f"Calibration Successful: {calibration_successful}")