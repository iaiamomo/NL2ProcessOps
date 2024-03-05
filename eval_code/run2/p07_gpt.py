from tools.crm_is import ReceiveOrder
from tools.manufacturer import BuySnacks
from tools.working_station_is import ScanOrder
from tools.manufacturer import OrderColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import AssembleInterior
from tools.smart_tester import TestSpindle
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import DeliverTestProtocol
from tools.pallet import PalletArrives
import threading

# Assuming the tools are already imported and available for use

def assemble_and_test_airplane(part_list, product_id):
    # Assemble the interior
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    
    # Test flight (assuming TestSpindle simulates this)
    test_passed = TestSpindle.call(product_id=product_id)
    
    # Create and send test protocol
    if test_passed:
        test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
        DeliverTestProtocol.call(product_id=product_id, protocol=test_protocol)
        return True, test_protocol
    else:
        return False, None

def process():
    # Receive order
    part_list, product_id = ReceiveOrder.call()
    
    # Manufacture parts in parallel
    threads = []
    for part in part_list:
        if part == "vodka bar":
            thread = threading.Thread(target=lambda: OrderColor.call(color=1))  # Example of ordering a part
        elif part == "whiskey bar":
            thread = threading.Thread(target=lambda: OrderColor.call(color=2))  # Example of ordering a different part
        # Add more conditions for other parts
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Assemble and test airplane
    assembly_successful, test_protocol = assemble_and_test_airplane(part_list, product_id)
    
    if assembly_successful:
        # Deliver airplane to customer
        print(f"Airplane {product_id} delivered with test protocol: {test_protocol}")
        # Assuming customer confirmation is automatic for simplicity
        return "Delivery confirmed"
    else:
        return "Assembly or test failed"

if __name__ == "__main__":
    result = process()
    print(result)