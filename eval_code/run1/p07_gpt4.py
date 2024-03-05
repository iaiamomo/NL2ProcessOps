from tools.crm_is import ReceiveOrder
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import AssembleInterior
from tools.manufacturer import OrderParts
from tools.manufacturer import CreateTestProtocol
import threading

# Assuming the tools are already imported and available for use

def manufacture_parts(part_list, product_id):
    # Inform storehouse and engineering departments about the parts and product id
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
    # Manufacturer orders the parts online
    OrderParts.call(part_list=part_list)

def assemble_and_test(part_list, product_id):
    # Assemble the interior of the plane
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    # Create the test protocol for the product
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    return test_protocol

def process():
    # Sales department receives a new order specification from customer
    part_list, product_id = ReceiveOrder.call()
    
    # Manufacture parts in parallel
    threads = []
    for _ in range(4):  # Assuming there are 4 different parts to manufacture in parallel
        thread = threading.Thread(target=manufacture_parts, args=(part_list, product_id))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Assemble interior and test
    test_protocol = assemble_and_test(part_list, product_id)
    
    # Deliver plane to customer and wait for confirmation
    # Assuming a function DeliverPlane exists for delivery and confirmation
    # This is a placeholder as the actual delivery and confirmation process is not detailed in the tools
    # DeliverPlane.call(product_id=product_id, test_protocol=test_protocol)
    
    return "Process completed successfully."

if __name__ == "__main__":
    result = process()
    print(result)