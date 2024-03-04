from tools.manufacturer import AssembleInterior
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import DeliverProduct
from tools.crm_is import AcceptOrder
import threading
from queue import Queue

# Assuming the tools are already imported as per the guidelines
# from tools import AssembleInterior, CreateTestProtocol, DeliverProduct, AcceptOrder

def manufacture_parts(part_list, product_id):
    # This function simulates the manufacturing of parts in parallel
    def manufacture_part(part):
        print(f"Manufacturing {part} for product {product_id}")
        # Simulate time taken to manufacture part
        # In real scenario, this could be a call to a specific manufacturing function

    threads = []
    for part in part_list:
        thread = threading.Thread(target=manufacture_part, args=(part,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"All parts manufactured for product {product_id}")

def process(product_id, part_list):
    # Receive customer specifications
    print("Received customer specifications")

    # Manufacture parts in parallel
    manufacture_parts(part_list, product_id)

    # Assemble interior
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    print("Interior assembled")

    # Test flight and create test protocol
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    print(f"Test protocol created: {test_protocol}")

    # Deliver plane to customer
    DeliverProduct.call(product_id=product_id)
    print("Plane delivered to customer")

    # Customer confirmation
    order_accepted = AcceptOrder.call(product_id=product_id)
    if order_accepted:
        print("Customer confirmed order")
    else:
        print("Customer did not confirm order")

    return order_accepted

if __name__ == "__main__":
    product_id = 123
    part_list = ["vodka bar", "whiskey bar", "seats", "toilet water system"]
    process_result = process(product_id, part_list)
    print(f"Process completed with result: {process_result}")