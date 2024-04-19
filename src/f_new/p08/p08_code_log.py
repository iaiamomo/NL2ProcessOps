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
from tools.worker import CheckTypeCardboard
from tools.worker import StoreCardboardRoll
from tools.vision_is import AnalyzeWarehouse
from tools.worker import InsertCardboardTypeInfo
from tools.wms_is import UpdateStock

import numpy as np

def capture_warehouse_image() -> np.matrix:
    return True

def process_new_cardboard_roll():
    CheckTypeCardboard.fake_call()
    InsertCardboardTypeInfo.fake_call()
    capture_warehouse_image()
    AnalyzeWarehouse.fake_call()
    StoreCardboardRoll.fake_call()
    UpdateStock.fake_call()

if __name__ == "__main__":
    process_new_cardboard_roll()
