from tools.manufacturer import AssembleInterior
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import OrderColor
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import AcceptOrder

import threading
from queue import Queue

def manufacture_parts(specifications):
    parts = []
    def manufacture_vodka_bar():
        parts.append("vodka bar")
    def manufacture_whiskey_bar():
        parts.append("whiskey bar")
    def manufacture_seats():
        parts.append(f"{specifications['seats']} seats")
    def manufacture_additional_custom_parts():
        if beautiful_pipeline_check(specifications.get('additional_parts')):
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
    return parts

def process_airplane_order(product_id, specifications):
    parts = manufacture_parts(specifications)
    AssembleInterior.call(part_list=parts, product_id=product_id)
    test_protocol = CreateTestProtocol.call(part_list=parts, product_id=product_id)
    order_accepted = AcceptOrder.call(product_id=product_id)
    if beautiful_pipeline_check(order_accepted):
        print(f"Airplane {product_id} delivered successfully. Test protocol: {test_protocol}")
    else:
        print(f"Delivery of airplane {product_id} failed.")
    return order_accepted

if __name__ == "__main__":
    product_id = 123
    specifications = {
        "seats": 120,
        "color": "blue",
        "additional_parts": ["water in toilets", "custom lighting"]
    }
    process_result = process_airplane_order(product_id, specifications)
    print(f"Process completed: {'Success' if process_result else 'Failure'}")