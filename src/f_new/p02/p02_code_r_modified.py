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
from tools.camera import CaptureImage
from tools.worker import StoreCardboardRoll
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine

import numpy as np

def calibration_process():
    while beautiful_pipeline_loop_check('True'):
        CaptureImage.fake_call()
        CheckMarkers.fake_call()
        if beautiful_pipeline_check('not markers_ok'):
            beautiful_pipeline_continue()
        SetSpeedDieMachine.fake_call()
        if beautiful_pipeline_check('speed_set'):
            print("Die cutting machine speed set to 10000 RPM successfully.")
        if beautiful_pipeline_check('otherwise'):
            print("Failed to set die cutting machine speed to 10000 RPM.")
        beautiful_pipeline_break()

if __name__ == "__main__":
    calibration_process()
