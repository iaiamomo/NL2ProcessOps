from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
from threading import Thread
from queue import Queue

# Assuming the tools are already imported as per the guidelines
# from tools import L12AssembleSpindle, RetrieveRawMaterials, L12SetUp, TestSpindle

def retrieve_and_setup(part_list, setup_queue, retrieve_queue):
    # Set up L12 line
    setup_result = L12SetUp.call()
    setup_queue.put(setup_result)

    # Retrieve raw materials
    retrieve_result = RetrieveRawMaterials.call(part_list=part_list)
    retrieve_queue.put(retrieve_result)

def process(part_list, product_id):
    setup_queue = Queue()
    retrieve_queue = Queue()

    # Start parallel tasks for setting up L12 line and retrieving raw materials
    thread = Thread(target=retrieve_and_setup, args=(part_list, setup_queue, retrieve_queue))
    thread.start()
    thread.join()

    # Check if both tasks were successful
    setup_result = setup_queue.get()
    retrieve_result = retrieve_queue.get()
    if setup_result and retrieve_result:
        # Assemble spindle
        assembly_result = L12AssembleSpindle.call(part_list=part_list)
        if assembly_result['assembled']:
            # Test and run-in spindle
            test_result = TestSpindle.call(product_id=product_id)
            if test_result['passed']:
                return "Process completed successfully."
            else:
                # Send spindle to maintenance
                return "Spindle sent to maintenance."
        else:
            return "Assembly failed."
    else:
        return "Setup or retrieval failed."

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    product_id = 123  # Example product ID
    result = process(part_list, product_id)
    print(result)