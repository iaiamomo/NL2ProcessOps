from tools.manufacturer import AssembleInterior
from tools.manufacturer import OrderColor
from tools.manufacturer import SendRequirements
from tools.smart_tester import TestSpindle
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import DeliverTestProtocol
from tools.crm_is import ReceiveOrder
from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import AssembleInterior, OrderColor, SendRequirements, TestSpindle, CreateTestProtocol, DeliverTestProtocol, ReceiveOrder

def order_parts(part_list):
    # This function simulates ordering parts by sending requirements to the proper teams
    SendRequirements.call(part_list=part_list)

def test_and_delivery(product_id, part_list):
    # Test the product
    test_passed = TestSpindle.call(product_id=product_id)
    if test_passed:
        # Create and send test protocol
        test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
        DeliverTestProtocol.call(product_id=product_id, protocol=test_protocol)
        print(f"Test protocol for product {product_id} sent to customer.")
    else:
        print(f"Product {product_id} failed the test.")

def process():
    # Receive order
    part_list, product_id = ReceiveOrder.call()
    
    # Order parts (bars, seats, seat colors, toilet water amount)
    order_parts(part_list)
    
    # Manufacture parts (Assuming this is done after ordering)
    # Here, we're directly moving to assembling as manufacturing details are abstracted
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    
    # Test and delivery process
    test_and_delivery_thread = Thread(target=test_and_delivery, args=(product_id, part_list))
    test_and_delivery_thread.start()
    test_and_delivery_thread.join()
    
    print(f"Airplane {product_id} delivered to customer and awaiting confirmation.")

if __name__ == "__main__":
    process()