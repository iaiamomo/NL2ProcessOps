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
from tools.mold_is import SensorMeasure
from tools.vision_is import CheckMarkers
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction

def check_parameters_against_standards():
    if beautiful_pipeline_check('temperature > 100 and pressure > 200 and fill_rate > 50'):
        return True
    if beautiful_pipeline_check('otherwise'):
        return True

def process_injection_molding():
    while beautiful_pipeline_loop_check('True'):
        SensorMeasure.fake_call()
        check_parameters_against_standards()
        if beautiful_pipeline_check('not parameters_ok'):
            AdjustMold.fake_call()
        if beautiful_pipeline_check('otherwise'):
            AuthorizeProduction.fake_call()
            beautiful_pipeline_break()  
            break

if __name__ == "__main__":
    process_injection_molding()
