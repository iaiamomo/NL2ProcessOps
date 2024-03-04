from tools.manufacturer import AssembleBicycle
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import OrderParts
from tools.worker import AssembleParts
from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import AcceptOrder, InformStorehouseEngineering, AssembleBicycle

def process_order(product_id, part_list):
    # Accept or reject the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order Rejected"

    # Inform Storehouse and Engineering Department
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Process each part in the part list
    for part in part_list:
        # Assuming a function check_part_availability that returns True if part is available, False otherwise
        part_available = check_part_availability(part)
        if part_available:
            reserve_part(part)
        else:
            back_order_part(part)

    # Prepare for assembly (Assuming this is done implicitly in the process)
    prepare_for_assembly()

    # Assemble the bicycle
    AssembleBicycle.call(part_list=part_list)

    # Ship the bicycle to the customer
    return "Bicycle Shipped to Customer"

def check_part_availability(part):
    # Placeholder function to simulate checking part availability
    # In a real scenario, this would interact with the storehouse's inventory system
    return True

def reserve_part(part):
    # Placeholder function to simulate reserving a part
    pass

def back_order_part(part):
    # Placeholder function to simulate back-ordering a part
    pass

def prepare_for_assembly():
    # Placeholder function to simulate preparation for assembly
    pass

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['frame', 'wheels', 'brakes']  # Example part list
    result = process_order(product_id, part_list)
    print(result)