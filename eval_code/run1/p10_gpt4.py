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
        # This is a simplification, as the actual logic for checking availability and reserving/back-ordering is not provided
        # Assume a function check_and_process_part(part) exists for this purpose
        check_and_process_part(part)
    # After processing all parts, inform that all parts are processed
    print("All parts processed.")

def prepare_for_assembling():
    # Simulate preparing for assembling
    # This is a simplification, as the actual logic for preparation is not provided
    # Assume a function prepare_assembly() exists for this purpose
    prepare_assembly()
    print("Preparation for assembling finished.")

def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        print("Order rejected.")
        return

    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Start parallel tasks for processing part list and preparing for assembling
    part_list_thread = threading.Thread(target=process_part_list, args=(part_list,))
    prepare_assembling_thread = threading.Thread(target=prepare_for_assembling)

    part_list_thread.start()
    prepare_assembling_thread.start()

    # Wait for both threads to complete
    part_list_thread.join()
    prepare_assembling_thread.join()

    # After both tasks are completed, proceed with assembling the bicycle
    AssembleBicycle.call(part_list=part_list)
    print("Bicycle assembled and ready to be shipped.")

    # Simulate shipping the bicycle
    # This is a simplification, as the actual logic for shipping is not provided
    # Assume a function ship_bicycle(product_id) exists for this purpose
    ship_bicycle(product_id)
    print("Bicycle shipped to customer.")

if __name__ == "__main__":
    process_order()