from tools.worker import CheckTypeCardboard
from tools.worker import StoreCardboardRoll
from tools.vision_is import AnalyzeWarehouse
from tools.wms_is import OrderRawMaterial
from tools.camera import CaptureImage
from tools.wms_is import UpdateStock
import numpy as np

class CheckTypeCardboard:
    @staticmethod
    def call():
        return {"type_cardboard": "white"}  # Example return, in practice, this would be dynamic

class StoreCardboardRoll:
    @staticmethod
    def call(location):
        pass  # In practice, this would store the cardboard roll at the specified location

class AnalyzeWarehouse:
    @staticmethod
    def call(image, type_cardboard):
        return {"location": "A1"}  # Example return, in practice, this would be dynamic based on the image and type

class CaptureImage:
    @staticmethod
    def call():
        return {"image": np.matrix([[0]])}  # Example return, in practice, this would capture and return a real image

class UpdateStock:
    @staticmethod
    def call(product_type):
        pass  # In practice, this would update the stock of the specified product type in the WMS

def process_new_cardboard_roll():
    # Check type of cardboard roll
    type_cardboard = CheckTypeCardboard.call()["type_cardboard"]
    
    # Enter information in WMS system is assumed to be part of the CheckTypeCardboard and UpdateStock steps
    
    # Capture image of warehouse
    image = CaptureImage.call()["image"]
    
    # Analyze image and identify storage location
    location = AnalyzeWarehouse.call(image, type_cardboard)["location"]
    
    # Store cardboard roll in identified location
    StoreCardboardRoll.call(location)
    
    # Update stock in WMS system
    UpdateStock.call(type_cardboard)

if __name__ == "__main__":
    process_new_cardboard_roll()