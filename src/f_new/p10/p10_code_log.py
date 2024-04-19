import sys
sys.path.append('./')
import threading

def beautiful_pipeline_parallel():
    print(f"beautiful_pipeline_parallel - {threading.get_ident()}")

def beautiful_pipeline_end_parallel():
    print(f"beautiful_pipeline_end_parallel - {threading.get_ident()}")

def beautiful_pipeline_break():
    print(f"beautiful_pipeline_break - {threading.get_ident()}")

def beautiful_pipeline_continue():
    print(f"beautiful_pipeline_continue - {threading.get_ident()}")

def beautiful_pipeline_check(condition):
    print(f"condition {condition} - {threading.get_ident()}")
    return True

def beautiful_pipeline_loop_check(condition):
    global loop_count
    if loop_count == 1:
        loop_count = 0
        return False
    elif loop_count == 0:
        loop_count += 1
        print(f"loop_count {loop_count} - condition {condition} - {threading.get_ident()}")
        return True
loop_count = 0
from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import ReceiveParts
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle

import threading

def process_part_list():
    for part in part_list:
        part_available = True  
        if beautiful_pipeline_check('part_available'):
            print(f"Reserving part: {part}")
        elif beautiful_pipeline_check('otherwise'):
            print(f"Back-ordering part: {part}")

def prepare_for_assembling():
    print("Preparing for assembling")

def process_order():
    ReceiveOrder.fake_call()
    AcceptOrder.fake_call()
    if beautiful_pipeline_check('not order_accepted'):
        print("Order rejected")
        return
    InformStorehouseEngineering.fake_call()
    beautiful_pipeline_parallel()
    threads = []
    thread_part_list = threading.Thread(target=process_part_list)
    thread_prepare = threading.Thread(target=prepare_for_assembling)
    threads.append(thread_part_list)
    threads.append(thread_prepare)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    beautiful_pipeline_end_parallel()
    AssembleBicycle.fake_call()
    print("Bicycle assembled")
    print("Bicycle shipped to customer")

if __name__ == "__main__":
    process_order()
