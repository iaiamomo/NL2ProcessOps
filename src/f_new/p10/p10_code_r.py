from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import ReceiveParts
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle

import threading

def process_part_list(part_list):
    for part in part_list:
        part_available = True  
        if beautiful_pipeline_check(part_available):
            print(f"Reserving part: {part}")
        else:
            print(f"Back-ordering part: {part}")

def prepare_for_assembling():
    print("Preparing for assembling")

def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if beautiful_pipeline_check(not order_accepted):
        print("Order rejected")
        return
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
    beautiful_pipeline_parallel()
    threads = []
    thread_part_list = threading.Thread(target=process_part_list, args=(part_list,))
    thread_prepare = threading.Thread(target=prepare_for_assembling)
    threads.append(thread_part_list)
    threads.append(thread_prepare)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    beautiful_pipeline_end_parallel()
    AssembleBicycle.call(part_list=part_list)
    print("Bicycle assembled")
    print("Bicycle shipped to customer")

if __name__ == "__main__":
    process_order()