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
        # This is a placeholder for the actual logic which might involve calling another tool or service
        print(f"Processing part: {part}")
        # Assume part is always successfully processed for simplicity
    print("All parts processed.")

def prepare_for_assembling():
    # Simulate preparing for assembling
    # This is a placeholder for the actual logic which might involve calling another tool or service
    print("Preparation for assembling done.")

def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        print("Order rejected.")
        return

    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Parallel execution of processing part list and preparing for assembling
    threads = []
    thread_part_list = threading.Thread(target=process_part_list, args=(part_list,))
    thread_prepare = threading.Thread(target=prepare_for_assembling)
    threads.append(thread_part_list)
    threads.append(thread_prepare)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    AssembleBicycle.call(part_list=part_list)
    print("Bicycle assembled and ready to be shipped.")

    # Simulate shipping bicycle
    print("Bicycle shipped to customer.")

if __name__ == "__main__":
    process_order()