from tools.worker import StoreCardboardRoll
from tools.vision_is import AnalyzeWarehouse
from tools.worker import CheckTypeCardboard
from tools.worker import InsertCardboardTypeInfo
from tools.wms_is import UpdateStock
import numpy as np

def process_new_cardboard_roll(image: np.matrix):
    """
    Process a new cardboard roll arriving at the warehouse.
    
    :param image: np.matrix, an image of the current status of the warehouse.
    """
    # Worker checks the type of cardboard
    type_cardboard = CheckTypeCardboard.call()
    
    # Worker inserts the type of cardboard in the system
    InsertCardboardTypeInfo.call(type_cardboard=type_cardboard)
    
    # System analyzes the warehouse to identify where to store the new cardboard roll
    location = AnalyzeWarehouse.call(image=image, type_cardboard=type_cardboard)
    
    # Worker stores the cardboard roll in the identified location in the warehouse
    StoreCardboardRoll.call(location=location)
    
    # Warehouse department updates the stock of that cardboard roll
    UpdateStock.call(product_type=type_cardboard)

if __name__ == "__main__":
    # Example usage
    # Assuming an image of the warehouse's current status is available as a numpy matrix
    warehouse_image = np.random.rand(100, 100)  # Placeholder for an actual image
    process_new_cardboard_roll(image=warehouse_image)