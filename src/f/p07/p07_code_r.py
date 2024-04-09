import threading
from queue import Queue
def manufacture_parts(part_list, product_id):
    print(f"Manufacturing parts for product {product_id}...")
def test_flight_and_create_protocol(part_list, product_id):
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    return test_protocol
def process():
    part_list, product_id = ReceiveOrder.call()
    threads = []
    parallel()
    for part in part_list:
        thread = threading.Thread(target=manufacture_parts, args=(part, product_id))
        threads.append(thread)
        thread.start()
    end_parallel()
    for thread in threads:
        thread.join()
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    test_protocol = test_flight_and_create_protocol(part_list, product_id)
    print(f"Delivering airplane {product_id} to customer...")
    print(f"Customer confirmation received for airplane {product_id}.")
    return test_protocol
if __name__ == "__main__":
    test_protocol = process()
    print(f"Test Protocol: {test_protocol}")