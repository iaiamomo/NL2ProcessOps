from tools.worker import CheckTypeCardboard
from tools.vision_is import AnalyzeWarehouse
from tools.worker import StoreCardboardRoll
from tools.wms_is import UpdateStock
import numpy as np

class CheckTypeCardboard:
    @staticmethod
    def call():
        return {"type_cardboard": "white"}  # Example return, in practice, this would be dynamic

class AnalyzeWarehouse:
    @staticmethod
    def call(image, type_cardboard):
        # Example return, in practice, this would analyze the image and type to determine location
        return {"location": "A1"}

class StoreCardboardRoll:
    @staticmethod
    def call(location):
        print(f"Cardboard roll stored at {location}")

class UpdateStock:
    @staticmethod
    def call(product_type):
        print(f"Stock updated for {product_type}")

def process_new_cardboard_roll(image: np.matrix):
    # Worker checks the type of cardboard
    type_cardboard_info = CheckTypeCardboard.call()
    type_cardboard = type_cardboard_info["type_cardboard"]
    
    # System analyzes the warehouse to identify storage location
    location_info = AnalyzeWarehouse.call(image, type_cardboard)
    location = location_info["location"]
    
    # Worker stores the cardboard roll in the identified location
    StoreCardboardRoll.call(location)
    
    # Warehouse department updates the stock
    UpdateStock.call(type_cardboard)
    
    print(f"New {type_cardboard} cardboard roll processed and stored at {location}.")

if __name__ == "__main__":
    # Simulate an image of the warehouse status
    warehouse_image = np.matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    
    process_new_cardboard_roll(warehouse_image)