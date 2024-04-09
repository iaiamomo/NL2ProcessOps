from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import AssembleInterior, CreateTestProtocol, ReceiveOrder

def manufacture_parts(part_list, product_id):
    # This function simulates the manufacturing of parts in parallel
    # Since the actual manufacturing functions are not provided, we assume they are handled internally
    pass

def test_flight_and_protocol(part_list, product_id):
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    return test_protocol

def process_airplane_order():
    # Receive airplane customization specifications
    part_list, product_id = ReceiveOrder.call()

    # Manufacture parts in parallel
    manufacture_thread = Thread(target=manufacture_parts, args=(part_list, product_id))
    manufacture_thread.start()
    manufacture_thread.join()

    # Assemble interior
    AssembleInterior.call(part_list=part_list, product_id=product_id)

    # Test flight and create test protocol
    test_protocol = test_flight_and_protocol(part_list, product_id)

    # Deliver plane to customer and wait for confirmation
    # Assuming delivery and confirmation are handled internally as the tools for these are not provided
    print(f"Test protocol for product {product_id}: {test_protocol}")
    print("Plane delivered to customer and awaiting confirmation.")

if __name__ == "__main__":
    process_airplane_order()