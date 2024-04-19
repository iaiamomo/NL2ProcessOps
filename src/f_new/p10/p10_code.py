from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import ReceiveParts
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle

import threading

# Assuming the tools are already imported and available for use as described

def process_part_list(part_list):
    for part in part_list:
        # Simulate checking if part is available and either reserving or back-ordering it
        # This is a simplification, as the actual logic for checking availability and reserving/back-ordering is not provided
        # In a real scenario, this would involve database queries or API calls
        part_available = True  # Placeholder for actual availability check
        if part_available:
            # Reserve part
            print(f"Reserving part: {part}")
        else:
            # Back-order part
            print(f"Back-ordering part: {part}")

def prepare_for_assembling():
    # Simulate preparation for assembling
    print("Preparing for assembling")

def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        print("Order rejected")
        return

    # Inform storehouse and engineering department
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Process part list and prepare for assembling in parallel
    threads = []
    thread_part_list = threading.Thread(target=process_part_list, args=(part_list,))
    thread_prepare = threading.Thread(target=prepare_for_assembling)
    threads.append(thread_part_list)
    threads.append(thread_prepare)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Assemble bicycle
    AssembleBicycle.call(part_list=part_list)
    print("Bicycle assembled")

    # Ship bicycle
    print("Bicycle shipped to customer")

if __name__ == "__main__":
    process_order()