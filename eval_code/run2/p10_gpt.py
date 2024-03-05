from tools.manufacturer import AssembleBicycle
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import OrderParts
from tools.worker import AssembleParts
from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import AcceptOrder, InformStorehouseEngineering, AssembleBicycle, CheckColorQuantity, OrderParts, AssembleParts

def process_order(product_id, part_list):
    # Accept or reject the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order Rejected"

    # Inform Storehouse and Engineering Department
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Process each part in the part list
    for part in part_list:
        # Assuming part is a dictionary with 'name' and 'quantity' keys
        # Check if part is available (mock function, replace with actual implementation)
        part_available = check_part_availability(part)
        if part_available:
            reserve_part(part)  # Mock function to reserve part
        else:
            back_order_part(part)  # Mock function to back-order part

    # Prepare for assembly (mock function, replace with actual implementation)
    prepare_for_assembly()

    # Assemble the bicycle
    AssembleBicycle.call(part_list=part_list)

    # Ship the bicycle to the customer (mock function, replace with actual implementation)
    ship_bicycle_to_customer()

    return "Order Processed and Bicycle Shipped"

def check_part_availability(part):
    # Mock implementation, replace with actual logic to check part availability
    return True

def reserve_part(part):
    # Mock implementation, replace with actual logic to reserve part
    pass

def back_order_part(part):
    # Mock implementation, replace with actual logic to back-order part
    pass

def prepare_for_assembly():
    # Mock implementation, replace with actual logic to prepare for assembly
    pass

def ship_bicycle_to_customer():
    # Mock implementation, replace with actual logic to ship bicycle
    pass

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = [{'name': 'wheel', 'quantity': 2}, {'name': 'frame', 'quantity': 1}]  # Example part list
    result = process_order(product_id, part_list)
    print(result)