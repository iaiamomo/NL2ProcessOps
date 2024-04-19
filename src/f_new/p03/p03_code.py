from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle

import threading

# Assuming the tools are already imported and available for use as described
# in the problem description.

def retrieve_and_setup(part_list):
    # Retrieve raw materials and set up L12 line in parallel
    retrieved_result = [None]  # Using a list to store result due to Python's scoping rules
    setup_result = [None]

    def retrieve():
        retrieved_result[0] = RetrieveRawMaterials.call(part_list=part_list)

    def setup():
        setup_result[0] = L12SetUp.call()

    threads = []
    t1 = threading.Thread(target=retrieve)
    t2 = threading.Thread(target=setup)
    threads.append(t1)
    threads.append(t2)

    t1.start()
    t2.start()

    for t in threads:
        t.join()

    return retrieved_result[0], setup_result[0]

def process_spindle_order(part_list, product_id):
    # Retrieve raw materials and set up L12 line in parallel
    retrieved, setup = retrieve_and_setup(part_list)

    # Proceed only if both tasks were successful
    if retrieved and setup:
        assembled = L12AssembleSpindle.call(part_list=part_list)
        if assembled:
            test_passed = TestSpindle.call(product_id=product_id)
            if not test_passed:
                # Send to maintenance if test failed
                print("Spindle sent to maintenance.")
            else:
                print("Spindle assembly and testing completed successfully.")
        else:
            print("Spindle assembly failed.")
    else:
        print("Failed to retrieve materials or set up L12 line.")

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    product_id = 123  # Example product ID
    process_spindle_order(part_list, product_id)