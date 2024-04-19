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
from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import CheckColorAvailability
from tools.manufacturer import OrderColor
from tools.printer_3d import HeatUpBedExtruder
from tools.printer_3d import TurnOn
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print

def instruct_artist_and_print_model():
    SendSketches.fake_call()
    ChoosePlasticColor.fake_call()
    CheckColorAvailability.fake_call()
    if beautiful_pipeline_check('color_availability'):
        CheckColorQuantity.fake_call()
        if beautiful_pipeline_check('quantity < 100'):
            pass
    if beautiful_pipeline_check('otherwise'):
        OrderColor.fake_call()
    TurnOn.fake_call()
    HeatUpBedExtruder.fake_call()
    GenerateGCode.fake_call()
    Print.fake_call()
if __name__ == "__main__":
    instruct_artist_and_print_model()
