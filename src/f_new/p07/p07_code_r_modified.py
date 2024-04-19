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

def beautiful_pipeline_check_elif(condition):
    print(f"condition elif {condition} - {threading.get_ident()}")
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
from tools.manufacturer import AssembleInterior
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import OrderColor
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import AcceptOrder

import threading
from queue import Queue

def manufacture_parts():
    parts = []
    def manufacture_vodka_bar():
        parts.append("vodka bar")
    def manufacture_whiskey_bar():
        parts.append("whiskey bar")
    def manufacture_seats():
        parts.append(f"{specifications['seats']} seats")
    def manufacture_additional_custom_parts():
        if beautiful_pipeline_check('specifications.get('additional_parts')'):
            parts.extend(specifications['additional_parts'])
    beautiful_pipeline_parallel()
    threads = [
        threading.Thread(target=manufacture_vodka_bar),
        threading.Thread(target=manufacture_whiskey_bar),
        threading.Thread(target=manufacture_seats),
        threading.Thread(target=manufacture_additional_custom_parts)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    beautiful_pipeline_end_parallel()
    return True

def process_airplane_order():
    manufacture_parts()
    AssembleInterior.fake_call()
    CreateTestProtocol.fake_call()
    AcceptOrder.fake_call()
    if beautiful_pipeline_check('order_accepted'):
        print(f"Airplane {product_id} delivered successfully. Test protocol: {test_protocol}")
    if beautiful_pipeline_check('otherwise'):
        print(f"Delivery of airplane {product_id} failed.")
    return True

if __name__ == "__main__":
    product_id = 123
    specifications = {
        "seats": 120,
        "color": "blue",
        "additional_parts": ["water in toilets", "custom lighting"]
    }
    process_airplane_order()
    print(f"Process completed: {'Success' if process_result if beautiful_pipeline_check('otherwise') 'Failure'}")
