from tools.worker import CheckTypeCardboard
from tools.worker import InsertCardboardTypeInfo
from tools.vision_is import AnalyzeWarehouse
from tools.worker import StoreCardboardRoll
import numpy as np

class CheckTypeCardboard:
    @staticmethod
    def call():
        return {"type_cardboard": "white"}  # Example return, in practice, this would be dynamic

class InsertCardboardTypeInfo:
    @staticmethod
    def call(type_cardboard):
        pass  # This would insert the type into the WMS system

class AnalyzeWarehouse:
    @staticmethod
    def call(image, type_cardboard):
        # Example logic, in practice, this would analyze the image
        if type_cardboard == "white":
            return {"location": "A1"}
        else:
            return {"location": "B1"}

class StoreCardboardRoll:
    @staticmethod
    def call(location):
        pass  # This would physically store the cardboard roll in the warehouse

def process_new_cardboard_roll(warehouse_image):
    # Worker checks the type of cardboard
    type_cardboard_info = CheckTypeCardboard.call()
    type_cardboard = type_cardboard_info["type_cardboard"]
    
    # Worker inserts the type of cardboard in the system
    InsertCardboardTypeInfo.call(type_cardboard)
    
    # System identifies where to store the new cardboard roll
    location_info = AnalyzeWarehouse.call(warehouse_image, type_cardboard)
    location = location_info["location"]
    
    # Worker stores the cardboard roll in the identified location
    StoreCardboardRoll.call(location)
    
    print(f"Cardboard roll of type '{type_cardboard}' stored in location '{location}'.")

if __name__ == "__main__":
    # Simulate an image of the current warehouse status
    warehouse_image = np.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])  # Placeholder for an actual image
    
    process_new_cardboard_roll(warehouse_image)