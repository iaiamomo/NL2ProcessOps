from tools.crm_is import ReceiveOrder
from tools.manufacturer import OrderColor
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleInterior
from tools.manufacturer import CreateTestProtocol
import threading

# Assuming the tools are already imported and available for use

def manufacture_parts(part_list, product_id):
    # Manufacture parts in parallel as per the process model
    threads = []
    for part in part_list:
        if part == "vodka bar":
            thread = threading.Thread(target=OrderParts.call, args=([part],))
            threads.append(thread)
        elif part == "whiskey bar":
            thread = threading.Thread(target=OrderParts.call, args=([part],))
            threads.append(thread)
        elif part == "seats":
            thread = threading.Thread(target=OrderParts.call, args=([part],))
            threads.append(thread)
        elif part == "additional custom parts":
            thread = threading.Thread(target=OrderParts.call, args=([part],))
            threads.append(thread)
        # Assuming there could be more parts, handle them generically
        else:
            thread = threading.Thread(target=OrderParts.call, args=([part],))
            threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def process():
    # Receive airplane customization specifications
    part_list, product_id = ReceiveOrder.call()
    
    # Manufacture parts (in parallel)
    manufacture_parts(part_list, product_id)
    
    # Assemble interior
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    
    # Test flight and create protocol
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    
    # Deliver plane to customer and wait for confirmation
    # Assuming a function DeliverPlane exists for delivery and confirmation
    # This is a placeholder for the delivery and confirmation process
    # DeliverPlane.call(product_id=product_id, test_protocol=test_protocol)
    
    return test_protocol

if __name__ == "__main__":
    test_protocol = process()
    print(f"Test Protocol: {test_protocol}")