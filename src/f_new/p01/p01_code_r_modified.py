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
from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.worker import AssembleParts

import threading

def display_scanning_ui_and_assemble_parts():
    DisplaysScanningUI.fake_call()
    AssembleParts.fake_call()

def process():
    EmptyScan.fake_call()
    ScanOrder.fake_call()
    beautiful_pipeline_parallel()
    thread_ui = threading.Thread(target=DisplaysScanningUI)
    thread_assemble = threading.Thread(target=AssembleParts)
    thread_ui.start()
    thread_assemble.start()
    thread_ui.join()
    thread_assemble.join()
    beautiful_pipeline_end_parallel()
    return True

if __name__ == "__main__":
    process()
    print(result)
