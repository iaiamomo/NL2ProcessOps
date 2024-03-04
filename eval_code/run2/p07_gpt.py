from tools.crm_is import ReceiveOrder
from tools.manufacturer import BuySnacks
from tools.working_station_is import ScanOrder
from tools.manufacturer import OrderColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import AssembleInterior
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import DeliverTestProtocol
from tools.smart_tester import TestSpindle
from tools.pallet import PalletArrives
import threading

def receive_order_and_dispatch():
    part_list, product_id = ReceiveOrder.call()
    # Assuming the part_list contains the specifications for bars, seats, color, and water amount
    # Dispatch manufacturing tasks based on the specifications
    threads = []
    for part in part_list:
        if part == "vodka bar":
            thread = threading.Thread(target=order_and_manufacture_vodka_bar)
            threads.append(thread)
        elif part == "whiskey bar":
            thread = threading.Thread(target=order_and_manufacture_whiskey_bar)
            threads.append(thread)
        elif part == "seats":
            thread = threading.Thread(target=order_and_manufacture_seats)
            threads.append(thread)
        elif part == "toilet water amount":
            thread = threading.Thread(target=order_and_manufacture_toilet_water)
            threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return part_list, product_id

def order_and_manufacture_vodka_bar():
    # Placeholder function for ordering and manufacturing vodka bar
    pass

def order_and_manufacture_whiskey_bar():
    # Placeholder function for ordering and manufacturing whiskey bar
    pass

def order_and_manufacture_seats():
    # Placeholder function for ordering and manufacturing seats
    pass

def order_and_manufacture_toilet_water():
    # Placeholder function for ordering and manufacturing toilet water amount
    pass

def assemble_interior_and_test_flight(part_list, product_id):
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    test_flight_passed = TestSpindle.call(product_id=product_id)
    if test_flight_passed:
        test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
        return test_protocol
    else:
        return "Test flight failed"

def deliver_and_confirm(product_id, test_protocol):
    DeliverTestProtocol.call(product_id=product_id, protocol=test_protocol)
    # Assuming a placeholder function for delivery and customer confirmation
    # In real scenario, this would involve logistics and customer interaction
    print(f"Airplane with ID {product_id} delivered and awaiting customer confirmation.")

def process():
    part_list, product_id = receive_order_and_dispatch()
    test_protocol = assemble_interior_and_test_flight(part_list, product_id)
    if test_protocol != "Test flight failed":
        deliver_and_confirm(product_id, test_protocol)
    else:
        print("Process aborted due to test flight failure.")

if __name__ == "__main__":
    process()