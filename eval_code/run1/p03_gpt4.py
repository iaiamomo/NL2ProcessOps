from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
import threading

# Assuming the tools are already imported and available for use as described
# in the problem description.

def retrieve_materials_and_setup_line(part_list):
    # Retrieve raw materials
    materials_retrieved = RetrieveRawMaterials.call(part_list=part_list)
    
    # Set up L12 line
    line_set_up = L12SetUp.call()
    
    return materials_retrieved, line_set_up

def process_spindle_order(part_list, product_id):
    # Retrieve materials and set up line in parallel
    thread_results = [None, None]
    
    def retrieve_materials():
        thread_results[0] = RetrieveRawMaterials.call(part_list=part_list)
    
    def setup_line():
        thread_results[1] = L12SetUp.call()
    
    t1 = threading.Thread(target=retrieve_materials)
    t2 = threading.Thread(target=setup_line)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    materials_retrieved, line_set_up = thread_results
    
    # Proceed only if both tasks were successful
    if materials_retrieved and line_set_up:
        # Assemble spindle
        assembly_successful = L12AssembleSpindle.call(part_list=part_list)
        
        if assembly_successful:
            # Test and run-in spindle
            test_passed = TestSpindle.call(product_id=product_id)
            
            if not test_passed:
                # Send to maintenance if test failed
                print("Spindle failed the test, sending to maintenance.")
            else:
                print("Spindle passed the test.")
        else:
            print("Assembly of spindle failed.")
    else:
        print("Failed to retrieve materials or set up the line.")

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    product_id = 123  # Example product ID
    process_spindle_order(part_list, product_id)