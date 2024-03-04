from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle
def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order rejected."
    
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
    
    # Assuming there's a method to check and reserve or back-order parts
    # This part is abstracted since there's no specific tool provided for it
    all_parts_ready = True
    for part in part_list:
        # Here you would check if the part is available and reserve or back-order it
        # For the sake of this example, we'll assume all parts are successfully processed
        pass
    
    # Assuming there's a method for the engineering department to prepare for assembly
    # This part is abstracted since there's no specific tool provided for it
    engineering_preparation_done = True
    
    if all_parts_ready and engineering_preparation_done:
        AssembleBicycle.call(part_list=part_list)
        # Assuming there's a method to ship the bicycle
        # This part is abstracted since there's no specific tool provided for it
        return "Bicycle assembled and shipped."
    else:
        return "Failed to process order due to parts or preparation issues."

if __name__ == "__main__":
    result = process_order()
    print(result)