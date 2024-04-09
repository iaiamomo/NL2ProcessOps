import numpy as np
def process_new_cardboard_roll():
    type_cardboard = CheckTypeCardboard.call()
    InsertCardboardTypeInfo.call(type_cardboard=type_cardboard)
    warehouse_image = capture_warehouse_image()
    location = AnalyzeWarehouse.call(image=warehouse_image, type_cardboard=type_cardboard)
    StoreCardboardRoll.call(location=location)
    UpdateStock.call(product_type=type_cardboard)
    return "Process completed successfully."
def capture_warehouse_image():
    return np.matrix([[0]])  
if __name__ == "__main__":
    result = process_new_cardboard_roll()
    print(result)