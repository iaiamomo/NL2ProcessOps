from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import L12AssembleSpindle, RetrieveRawMaterials, L12SetUp, TestSpindle

def retrieve_and_setup(part_list):
    # Retrieve raw materials and set up L12 line in parallel
    retrieved = RetrieveRawMaterials.call(part_list=part_list)
    set_up = L12SetUp.call()
    return retrieved, set_up

def assemble_test_maintenance(part_list):
    # Assemble spindle
    assembled = L12AssembleSpindle.call(part_list=part_list)
    if not assembled:
        return False, "Assembly failed"
    
    # Test and run-in spindle
    test_passed = TestSpindle.call(product_id=123)  # Assuming a fixed product ID for simplicity
    if not test_passed:
        # Send spindle to maintenance (assuming maintenance is a simple notification step here)
        print("Spindle sent to maintenance")
        return False, "Test failed and sent to maintenance"
    
    return True, "Process completed successfully"

def process(part_list):
    # Retrieve raw materials and set up L12 line in parallel
    retrieve_thread = threading.Thread(target=retrieve_and_setup, args=(part_list,))
    retrieve_thread.start()
    retrieve_thread.join()
    
    # Proceed with assembly, testing, and possibly maintenance
    success, message = assemble_test_maintenance(part_list)
    
    return success, message

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    success, message = process(part_list)
    print(f"Process status: {success}, Message: {message}")