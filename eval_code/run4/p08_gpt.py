from tools.worker import CheckTypeCardboard
from tools.wms_is import OrderRawMaterial
from tools.vision_is import AnalyzeWarehouse
from tools.worker import StoreCardboardRoll
import numpy as np

# Assuming the necessary tool classes are already imported as per the guidelines.

def process_new_cardboard_roll(image: np.matrix):
    # Check the type of cardboard roll
    type_cardboard = CheckTypeCardboard.call()
    
    # Enter information in WMS system (This step is described in the process but no specific tool is provided for it. 
    # Assuming it's part of the CheckTypeCardboard or an automated step not requiring explicit coding)
    
    # Capture image of warehouse and Analyze image to identify storage location
    # Since the image is already provided as an argument, we skip the capture part and directly analyze
    location = AnalyzeWarehouse.call(image=image, type_cardboard=type_cardboard)
    
    # Store cardboard roll in identified location
    StoreCardboardRoll.call(location=location)
    
    # Update stock in WMS system (This step is described in the process but no specific tool is provided for it. 
    # Assuming it's an automated step not requiring explicit coding or part of the StoreCardboardRoll)
    
    return "Process completed successfully."

if __name__ == "__main__":
    # Example usage
    # Assuming an image of the warehouse is available as a numpy matrix
    warehouse_image = np.matrix([[0, 0, 1], [1, 1, 0], [0, 1, 0]])
    result = process_new_cardboard_roll(image=warehouse_image)
    print(result)