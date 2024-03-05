from tools.worker import CheckTypeCardboard
from tools.worker import StoreCardboardRoll
from tools.vision_is import AnalyzeWarehouse
from tools.wms_is import OrderRawMaterial
from tools.camera import CaptureImage
from tools.wms_is import UpdateStock
import numpy as np

# Assuming the tools are already imported and available for use as described.
# Each tool can be called using <ToolName>.call(<input_parameters_if_any>)

def process_warehouse_new_cardboard_roll():
    # Worker checks the type of cardboard roll
    type_cardboard = CheckTypeCardboard.call()
    
    # Enter information in WMS system (Assuming this is handled internally and does not require explicit coding)
    
    # Capture image of warehouse
    warehouse_image = CaptureImage.call()
    
    # Analyze image and identify storage location
    location = AnalyzeWarehouse.call(image=warehouse_image, type_cardboard=type_cardboard)
    
    # Store cardboard roll in identified location
    StoreCardboardRoll.call(location=location)
    
    # Update stock in WMS system
    UpdateStock.call(product_type=type_cardboard)
    
    return "Process completed successfully."

if __name__ == "__main__":
    result = process_warehouse_new_cardboard_roll()
    print(result)