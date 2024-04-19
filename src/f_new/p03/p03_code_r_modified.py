import sys
sys.path.append('./')
import threading

def beautiful_pipeline_parallel():
    print(f"beautiful_pipeline_parallel - {threading.get_ident()}")

def beautiful_pipeline_end_parallel():
    print(f"beautiful_pipeline_end_parallel - {threading.get_ident()}")

def beautiful_pipeline_break():
    print(f"beautiful_pipeline_break - {threading.get_ident()}")

def beautiful_pipeline_continue():
    print(f"beautiful_pipeline_continue - {threading.get_ident()}")

def beautiful_pipeline_check(condition):
    print(f"condition {condition} - {threading.get_ident()}")
    return True

def beautiful_pipeline_check_elif(condition):
    print(f"condition elif {condition} - {threading.get_ident()}")
    return True

def beautiful_pipeline_loop_check(condition):
    global loop_count
    if loop_count == 1:
        loop_count = 0
        return False
    elif loop_count == 0:
        loop_count += 1
        print(f"loop_count {loop_count} - condition {condition} - {threading.get_ident()}")
        return True
loop_count = 0
from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle

import threading

def retrieve_and_setup():
    retrieved_result = [None]  
    setup_result = [None]
    def retrieve():
        RetrieveRawMaterials.fake_call()
    def setup():
        L12SetUp.fake_call()
    
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
    
    return True

def process_spindle_order():
    retrieve_and_setup()
    if beautiful_pipeline_check('retrieved and setup'):  # Modified if statement
        L12AssembleSpindle.fake_call()
        if beautiful_pipeline_check('assembled'):  # Modified if statement
            TestSpindle.fake_call()
            if beautiful_pipeline_check('not test_passed'):  # Modified if statement
                print("Spindle sent to maintenance.")
            if beautiful_pipeline_check('otherwise'):
                print("Spindle assembly and testing completed successfully.")
        if beautiful_pipeline_check('otherwise'):
            print("Spindle assembly failed.")
    if beautiful_pipeline_check('otherwise'):
        print("Failed to retrieve materials or set up L12 line.")

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  
    product_id = 123  
    process_spindle_order(part_list, product_id)
