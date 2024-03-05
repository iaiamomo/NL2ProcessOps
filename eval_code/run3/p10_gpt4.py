from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle
import threading

def process_part_list(part_list):
    for part in part_list:
        # Simulate checking if part is available and either reserving or back-ordering it
        # This is a simplification, in a real scenario, we would call a service or a database to check part availability
        part_available = True  # Assume part is available for demonstration purposes
        if part_available:
            print(f"Reserving part: {part}")
            # ReservePart.call(part)  # Example of how you would call the tool, assuming it exists
        else:
            print(f"Back-ordering part: {part}")
            # BackOrderPart.call(part)  # Example of how you would call the tool, assuming it exists

def prepare_for_assembling():
    print("Preparing for assembling...")

def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        print("Order rejected.")
        return

    # Inform storehouse and engineering department
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Parallel execution of processing part list and preparing for assembling
    part_list_thread = threading.Thread(target=process_part_list, args=(part_list,))
    prepare_thread = threading.Thread(target=prepare_for_assembling)

    part_list_thread.start()
    prepare_thread.start()

    part_list_thread.join()
    prepare_thread.join()

    # Assemble the bicycle
    AssembleBicycle.call(part_list=part_list)
    print("Bicycle assembled.")

    # Ship the bicycle
    print("Bicycle shipped to the customer.")

if __name__ == "__main__":
    process_order()