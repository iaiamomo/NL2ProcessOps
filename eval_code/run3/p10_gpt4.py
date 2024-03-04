from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle
import threading

# Assuming the tools are already imported and available for use as described.

def process_part_list(part_list):
    for part in part_list:
        # Simulate checking if part is available and either reserving or back-ordering it.
        # This is a simplification, as the actual decision logic and storage updates are not detailed.
        # In a real scenario, this would involve database operations or API calls.
        part_available = True  # Placeholder for actual availability check
        if part_available:
            # Reserve part
            pass  # Placeholder for reservation logic
        else:
            # Back-order part
            pass  # Placeholder for back-order logic

def prepare_for_assembling():
    # Placeholder for the actual preparation logic.
    # This could involve setting up assembly lines, gathering tools, etc.
    pass

def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order Rejected"

    # Informing storehouse and engineering department is done in parallel with processing part list and preparing for assembling.
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Using threads to simulate parallel tasks.
    part_list_thread = threading.Thread(target=process_part_list, args=(part_list,))
    prepare_thread = threading.Thread(target=prepare_for_assembling)

    part_list_thread.start()
    prepare_thread.start()

    # Wait for both threads to complete.
    part_list_thread.join()
    prepare_thread.join()

    # Assuming all parts are either reserved or back-ordered successfully and preparation is done.
    AssembleBicycle.call(part_list=part_list)
    # Assuming shipping is handled internally after assembly.
    return "Order Completed and Shipped"

if __name__ == "__main__":
    result = process_order()
    print(result)