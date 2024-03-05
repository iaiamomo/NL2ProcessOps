from tools.crm_is import ReceiveOrder
from tools.manufacturer import BuySnacks
from tools.working_station_is import ScanOrder
from tools.manufacturer import OrderColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import AssembleInterior
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import DeliverTestProtocol
from tools.pallet import PalletArrives
import threading

# Assuming the tools are already imported and available for use

def assemble_and_test_airplane(part_list, product_id):
    # Assemble the interior of the plane
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    
    # Create the test protocol
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    
    # Deliver the test protocol to the customer
    DeliverTestProtocol.call(product_id=product_id, protocol=test_protocol)

def process():
    # Sales department receives a new order specification from customer
    part_list, product_id = ReceiveOrder.call()
    
    # Manufacturing parts in parallel
    threads = []
    for part in part_list:
        if part == "vodka bar":
            thread = threading.Thread(target=lambda: None)  # Placeholder for actual manufacturing function
        elif part == "whiskey bar":
            thread = threading.Thread(target=lambda: None)  # Placeholder for actual manufacturing function
        elif part == "seats":
            thread = threading.Thread(target=lambda: None)  # Placeholder for actual manufacturing function
        elif part == "toilet water amount":
            thread = threading.Thread(target=lambda: None)  # Placeholder for actual manufacturing function
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Assemble the interior and test the airplane
    assemble_and_test_airplane(part_list, product_id)
    
    # Assuming the customer confirms delivery in another process not depicted here
    return "Airplane delivered and confirmed by the customer"

if __name__ == "__main__":
    result = process()
    print(result)