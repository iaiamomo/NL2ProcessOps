from tools.manufacturer import AssembleInterior
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import OrderColor
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import AcceptOrder

import threading
from queue import Queue

# Assuming the tools are already imported as per the guidelines
# from tools import AssembleInterior, CreateTestProtocol, AcceptOrder

def manufacture_parts(specifications):
    # This function simulates the manufacturing of different parts in parallel
    # It returns a list of manufactured parts
    parts = []
    def manufacture_vodka_bar():
        # Simulate manufacturing vodka bar
        parts.append("vodka bar")
    
    def manufacture_whiskey_bar():
        # Simulate manufacturing whiskey bar
        parts.append("whiskey bar")
    
    def manufacture_seats():
        # Simulate manufacturing seats based on specifications
        parts.append(f"{specifications['seats']} seats")
    
    def manufacture_additional_custom_parts():
        # Simulate manufacturing additional custom parts
        if specifications.get('additional_parts'):
            parts.extend(specifications['additional_parts'])
    
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
    
    return parts

def process_airplane_order(product_id, specifications):
    # Step 1: Manufacture parts in parallel
    parts = manufacture_parts(specifications)
    
    # Step 2: Assemble interior
    AssembleInterior.call(part_list=parts, product_id=product_id)
    
    # Step 3: Test flight and create protocol
    test_protocol = CreateTestProtocol.call(part_list=parts, product_id=product_id)
    
    # Step 4: Deliver airplane to customer and wait for confirmation
    order_accepted = AcceptOrder.call(product_id=product_id)
    
    if order_accepted:
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