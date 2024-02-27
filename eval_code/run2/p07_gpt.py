from tools.crm_is import ReceiveOrder
from tools.manufacturer import OrderColor
from tools.manufacturer import AssembleInterior
from tools.manufacturer import ReceiveParts
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import DeliverTestProtocol
from tools.pallet import PalletArrives
import threading

# Assuming the tools are already imported and available for use

def receive_order():
    part_list, product_id = ReceiveOrder.call()
    return part_list, product_id

def order_parts(part_list):
    # Example of ordering parts based on the part_list
    # This is a simplified version and does not cover all the logic
    for part in part_list:
        if part == "vodka bar":
            # Order vodka bar (assuming a method exists for this)
            pass
        elif part == "whiskey bar":
            # Order whiskey bar
            pass
        # Add more conditions for other parts like seats, toilet water amount, etc.
    
    # Assuming a method to wait for all parts to be manufactured and received
    ReceiveParts.call()

def assemble_interior(part_list, product_id):
    AssembleInterior.call(part_list=part_list, product_id=product_id)

def test_flight_and_delivery(part_list, product_id):
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    DeliverTestProtocol.call(product_id=product_id, protocol=test_protocol)
    # Assuming a method exists for delivering the airplane to the customer and receiving confirmation
    # DeliverAirplane.call(product_id=product_id)
    # ReceiveConfirmation.call(product_id=product_id)

def process():
    part_list, product_id = receive_order()
    order_parts_thread = threading.Thread(target=order_parts, args=(part_list,))
    order_parts_thread.start()
    order_parts_thread.join()  # Wait for parts ordering and manufacturing to complete
    
    assemble_interior(part_list, product_id)
    test_flight_and_delivery(part_list, product_id)
    return "Process completed successfully."

if __name__ == "__main__":
    result = process()
    print(result)