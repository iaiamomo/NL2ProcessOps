from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle
from threading import Thread

# Assuming the tools are already imported and available for use as described
def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    
    if not order_accepted:
        return "Order Rejected"
    
    # Inform storehouse and engineering department in parallel
    inform_thread = Thread(target=InformStorehouseEngineering.call, args=(part_list, product_id))
    inform_thread.start()
    inform_thread.join()
    
    # Process part list and prepare for assembling in parallel
    def process_part_list(part_list):
        for part in part_list:
            # Assuming CheckPartAvailability is a tool that checks if a part is available and returns a boolean
            part_available = CheckPartAvailability.call(part=part)
            if part_available:
                ReservePart.call(part=part)
            else:
                BackOrderPart.call(part=part)
    
    def prepare_for_assembling():
        # Assuming PrepareForAssembling is a tool that prepares everything for assembling
        PrepareForAssembling.call()
    
    part_list_thread = Thread(target=process_part_list, args=(part_list,))
    prepare_thread = Thread(target=prepare_for_assembling)
    
    part_list_thread.start()
    prepare_thread.start()
    
    part_list_thread.join()
    prepare_thread.join()
    
    # Assemble the bicycle
    AssembleBicycle.call(part_list=part_list)
    
    # Ship the bicycle
    # Assuming ShipBicycle is a tool that ships the bicycle
    ShipBicycle.call(product_id=product_id)
    
    return "Order Completed and Shipped"

if __name__ == "__main__":
    result = process_order()
    print(result)