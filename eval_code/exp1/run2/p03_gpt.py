from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import L12AssembleSpindle, RetrieveRawMaterials, L12SetUp, TestSpindle

def retrieve_and_setup(part_list):
    # Retrieve raw materials
    retrieved = RetrieveRawMaterials.call(part_list=part_list)
    # Set up L12 line
    set_up = L12SetUp.call()
    return retrieved, set_up

def assemble_test_maintenance(part_list, product_id):
    # Assemble spindle
    assembled = L12AssembleSpindle.call(part_list=part_list)
    if not assembled:
        return False, "Assembly failed"
    
    # Test and run-in spindle
    test_passed = TestSpindle.call(product_id=product_id)
    if not test_passed:
        # Send spindle to maintenance
        return False, "Sent to maintenance"
    
    return True, "Process completed successfully"

def process(part_list, product_id):
    # Retrieve raw materials and set up L12 line in parallel
    thread = threading.Thread(target=retrieve_and_setup, args=(part_list,))
    thread.start()
    thread.join()
    retrieved, set_up = thread.result()

    if not retrieved or not set_up:
        return False, "Failed to retrieve materials or set up L12 line"
    
    # Proceed with assembly, testing, and possibly maintenance
    success, message = assemble_test_maintenance(part_list, product_id)
    return success, message

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]
    product_id = 123
    success, message = process(part_list, product_id)
    print(f"Process status: {success}, Message: {message}")