from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
import threading

# Assuming the tools are already imported and available for use
# from tools import L12AssembleSpindle, RetrieveRawMaterials, L12SetUp, TestSpindle

def retrieve_materials_and_setup_line(part_list):
    # Retrieve raw materials
    materials_retrieved = RetrieveRawMaterials.call(part_list=part_list)
    # Set up L12 line
    line_set_up = L12SetUp.call()
    return materials_retrieved, line_set_up

def process(part_list, product_id):
    # Start the process by retrieving materials and setting up the line in parallel
    thread = threading.Thread(target=retrieve_materials_and_setup_line, args=(part_list,))
    thread.start()
    thread.join()
    materials_retrieved, line_set_up = thread.result()

    # Check if both tasks were successful
    if materials_retrieved and line_set_up:
        # Assemble the spindle
        assembly_success = L12AssembleSpindle.call(part_list=part_list)
        if assembly_success:
            # Test and run-in the spindle
            test_passed = TestSpindle.call(product_id=product_id)
            if test_passed:
                return "Process completed successfully."
            else:
                # If test failed, send spindle to maintenance (not explicitly modeled, so we just print a message)
                return "Spindle sent to maintenance."
        else:
            return "Assembly failed."
    else:
        return "Failed to retrieve materials or set up the line."

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    product_id = 123  # Example product ID
    result = process(part_list, product_id)
    print(result)