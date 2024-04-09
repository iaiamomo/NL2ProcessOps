import threading
from queue import Queue

# Assuming the tools are already imported as per the guidelines
# from tools import AssembleInterior, CreateTestProtocol, ReceiveOrder

def manufacture_parts(part_list, product_id):
    # This function simulates the manufacturing of parts in parallel
    # It's a placeholder for the actual calls to different teams based on part_list
    print(f"Manufacturing parts for product {product_id}...")

def test_flight_and_create_protocol(part_list, product_id):
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    return test_protocol

def process():
    # Receive order
    part_list, product_id = ReceiveOrder.call()

    # Manufacture parts in parallel
    threads = []
    for part in part_list:
        thread = threading.Thread(target=manufacture_parts, args=(part, product_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Assemble interior
    AssembleInterior.call(part_list=part_list, product_id=product_id)

    # Test flight and create protocol
    test_protocol = test_flight_and_create_protocol(part_list, product_id)

    # Deliver airplane to customer and wait for confirmation
    # This part is simplified as the delivery and confirmation process is not detailed in the tools
    print(f"Delivering airplane {product_id} to customer...")
    print(f"Customer confirmation received for airplane {product_id}.")

    return test_protocol

if __name__ == "__main__":
    test_protocol = process()
    print(f"Test Protocol: {test_protocol}")