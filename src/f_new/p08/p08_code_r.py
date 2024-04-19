from tools.worker import CheckTypeCardboard
from tools.worker import StoreCardboardRoll
from tools.vision_is import AnalyzeWarehouse
from tools.worker import InsertCardboardTypeInfo
from tools.wms_is import UpdateStock

import numpy as np

def capture_warehouse_image() -> np.matrix:
    return np.matrix([])

def process_new_cardboard_roll():
    type_cardboard = CheckTypeCardboard.call()
    InsertCardboardTypeInfo.call(type_cardboard=type_cardboard)
    warehouse_image = capture_warehouse_image()
    location = AnalyzeWarehouse.call(image=warehouse_image, type_cardboard=type_cardboard)
    StoreCardboardRoll.call(location=location)
    UpdateStock.call(product_type=type_cardboard)

if __name__ == "__main__":
    process_new_cardboard_roll()