from tools.worker import CheckTypeCardboard
from tools.worker import StoreCardboardRoll
from tools.wms_is import OrderRawMaterial
from tools.camera import CaptureImage
from tools.vision_is import AnalyzeWarehouse
from tools.wms_is import UpdateStock
import numpy as np

# Assuming the tools are already imported and available for use
def process_new_cardboard_roll():
    # Worker checks the type of cardboard roll
    type_cardboard = CheckTypeCardboard.call()
    
    # Enter information in WMS system (Assuming this is done implicitly as part of the process and not requiring explicit code)
    
    # Capture image of warehouse
    image = CaptureImage.call()
    
    # Analyze image and identify storage location
    location = AnalyzeWarehouse.call(image=image, type_cardboard=type_cardboard)
    
    # Worker stores the cardboard roll in the identified location
    StoreCardboardRoll.call(location=location)
    
    # Update stock in WMS system
    UpdateStock.call(product_type=type_cardboard)
    
    return "Process completed successfully."

if __name__ == "__main__":
    result = process_new_cardboard_roll()
    print(result)