from tools.worker import StoreCardboardRoll
from tools.vision_is import AnalyzeWarehouse
from tools.worker import CheckTypeCardboard
from tools.worker import InsertCardboardTypeInfo
from tools.wms_is import UpdateStock
import numpy as np

# Assuming the necessary tool classes are imported as per the guidelines
# StoreCardboardRoll, AnalyzeWarehouse, CheckTypeCardboard, InsertCardboardTypeInfo, UpdateStock

def process_new_cardboard_roll(image_of_warehouse: np.matrix):
    # Worker checks the type of cardboard
    type_cardboard = CheckTypeCardboard.call()
    
    # Worker inserts the type of cardboard in the system
    InsertCardboardTypeInfo.call(type_cardboard=type_cardboard)
    
    # Identify where to store a new cardboard roll
    location = AnalyzeWarehouse.call(image=image_of_warehouse, type_cardboard=type_cardboard)
    
    # Worker stores the cardboard roll in the warehouse
    StoreCardboardRoll.call(location=location)
    
    # Warehouse department updates the stock of a product
    UpdateStock.call(product_type=type_cardboard)
    
    print(f"Cardboard roll of type {type_cardboard} stored successfully at location {location}.")

if __name__ == "__main__":
    # Example usage
    # Assuming an image of the warehouse is available as a numpy matrix
    example_warehouse_image = np.matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    process_new_cardboard_roll(example_warehouse_image)