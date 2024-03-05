from tools.crm_is import ReceiveOrder
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import AssembleInterior
from tools.manufacturer import OrderParts
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import AcceptOrder
import threading
from queue import Queue

# Assuming the tools are already imported and available for use

def manufacture_parts(part_list, product_id):
    # Inform storehouse and engineering departments about the parts and product id
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
    # Order parts online based on the part list
    OrderParts.call(part_list=part_list)

def assemble_and_test(product_id, part_list):
    # Assemble the interior of the plane
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    # Create the test protocol
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    return test_protocol

def process():
    # Receive airplane customization specifications
    part_list, product_id = ReceiveOrder.call()

    # Manufacture parts in parallel
    threads = []
    q = Queue()

    def worker():
        while not q.empty():
            item = q.get()
            if item:
                manufacture_parts(part_list, product_id)
                q.task_done()

    for _ in range(4):  # Assuming there are 4 different parts to manufacture
        q.put(True)
    for _ in range(4):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Assemble interior and test
    test_protocol = assemble_and_test(product_id, part_list)

    # Deliver plane to customer and wait for confirmation
    order_accepted = AcceptOrder.call(product_id=product_id)
    if order_accepted:
        print(f"Plane with product ID {product_id} delivered successfully.")
        print(f"Test Protocol: {test_protocol}")
    else:
        print(f"Delivery of plane with product ID {product_id} failed.")

if __name__ == "__main__":
    process()