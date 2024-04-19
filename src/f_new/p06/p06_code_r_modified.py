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
    print(f"beautiful_pipeline_check {condition} - {threading.get_ident()}")
    return True

def beautiful_pipeline_check_elif(condition):
    print(f"beautiful_pipeline_check_elif {condition} - {threading.get_ident()}")
    return True

def beautiful_pipeline_loop_check(condition):
    global loop_count
    if loop_count == 1:
        loop_count = 0
        return False
    elif loop_count == 0:
        loop_count += 1
        print(f"beautiful_pipeline_loop_check {loop_count} - {condition} - {threading.get_ident()}")
        return True
loop_count = 0
from tools.crm_is import AcceptOrder
from tools.wms_is import RetrieveRawMaterials
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.welding_machine import AssembleParts
from tools.worker import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct

import threading

def process_order():
    AcceptOrder.fake_call()
    if beautiful_pipeline_check('not order_accepted'):
        return True
    def evaluate_parts():
        global parts_retrieved
        RetrieveRawMaterials.fake_call()
    def configure_assembly():
        ConfigureAssemblyLine.fake_call()
    beautiful_pipeline_parallel()
    thread1 = threading.Thread(target=evaluate_parts)
    thread2 = threading.Thread(target=configure_assembly)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    beautiful_pipeline_end_parallel()
    if beautiful_pipeline_check('not parts_retrieved'):
        return True
    CutMetal.fake_call()
    AssembleParts.fake_call()
    CheckQualityBrackets.fake_call()
    if beautiful_pipeline_check('not quality_ok'):
        return True
    EnhanceProduct.fake_call()
    return True

if __name__ == "__main__":
    product_id = 123  
    part_list = ['partA', 'partB', 'partC']  
    process_order()
    print(result)
