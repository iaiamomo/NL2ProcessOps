from tools.manufacturer import AssembleBicycle
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import OrderParts
from tools.worker import AssembleParts
from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import AcceptOrder, InformStorehouseEngineering, AssembleBicycle, OrderParts

def process_order(product_id, part_list):
    # Accept or reject the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order Rejected"

    # Inform Storehouse and Engineering Department
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Process Part List (Simulated here as a loop, assuming a function exists to check each part's availability)
    parts_processed = process_part_list(part_list)

    # Prepare for Assembly and Assemble Bicycle in parallel
    if parts_processed:
        prepare_and_assemble(part_list)

    return "Order Processed and Shipped"

def process_part_list(part_list):
    # Simulate checking each part's availability and ordering if not available
    for part in part_list:
        # Assuming a function exists to check part availability and order if necessary
        # This is a placeholder for the actual logic
        part_available = True  # Placeholder for actual check
        if not part_available:
            OrderParts.call(part_list=[part])
    return True

def prepare_and_assemble(part_list):
    # Prepare for Assembly and Assemble Bicycle in parallel
    # Assuming the preparation is part of the assembly process
    assembly_thread = Thread(target=AssembleBicycle.call, args=(part_list,))
    assembly_thread.start()
    assembly_thread.join()

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['wheel', 'frame', 'pedal']  # Example part list
    result = process_order(product_id, part_list)
    print(result)