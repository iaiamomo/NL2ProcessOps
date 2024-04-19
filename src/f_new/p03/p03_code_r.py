from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle

import threading

def retrieve_and_setup(part_list):
    retrieved_result = [None]  
    setup_result = [None]
    def retrieve():
        retrieved_result[0] = RetrieveRawMaterials.call(part_list=part_list)
    def setup():
        setup_result[0] = L12SetUp.call()
    
    beautiful_pipeline_parallel()  # Added before thread execution
    
    threads = []
    t1 = threading.Thread(target=retrieve)
    t2 = threading.Thread(target=setup)
    threads.append(t1)
    threads.append(t2)
    t1.start()
    t2.start()
    for t in threads:
        t.join()
    
    beautiful_pipeline_end_parallel()  # Added after thread execution
    
    return retrieved_result[0], setup_result[0]

def process_spindle_order(part_list, product_id):
    retrieved, setup = retrieve_and_setup(part_list)
    if beautiful_pipeline_check(retrieved and setup):  # Modified if statement
        assembled = L12AssembleSpindle.call(part_list=part_list)
        if beautiful_pipeline_check(assembled):  # Modified if statement
            test_passed = TestSpindle.call(product_id=product_id)
            if beautiful_pipeline_check(not test_passed):  # Modified if statement
                print("Spindle sent to maintenance.")
            else:
                print("Spindle assembly and testing completed successfully.")
        else:
            print("Spindle assembly failed.")
    else:
        print("Failed to retrieve materials or set up L12 line.")

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  
    product_id = 123  
    process_spindle_order(part_list, product_id)