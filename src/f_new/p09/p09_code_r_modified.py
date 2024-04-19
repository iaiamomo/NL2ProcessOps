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
from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.wms_is import RetrieveRawMaterials
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendInvitations
from tools.manufacturer import BuySnacks

import threading

def collect_and_refine_requirements():
    GenerateRequirementTreeHouse.fake_call()
    refined_part_list = part_list
    additional_requirements = True  
    while beautiful_pipeline_loop_check('additional_requirements'):
        RefineRequirementsTreeHouse.fake_call()
        additional_requirements = False  
    return True

def order_materials():
    OrderParts.fake_call()

def message_friends_for_help():
    friends_list = ["Alice", "Bob", "Charlie"]
    SendRequirements.fake_call()

def build_tree_house():
    AssembleTreeHouse.fake_call()

def send_party_invitations():
    people_list = ["Alice", "Bob", "Charlie", "Dana"]
    SendInvitations.fake_call()
    return True

def buy_snacks():
    BuySnacks.fake_call()

def tree_house_construction_process():
    collect_and_refine_requirements()
    beautiful_pipeline_parallel()
    order_thread = threading.Thread(target=order_materials, args=(refined_part_list,))
    message_thread = threading.Thread(target=message_friends_for_help)
    order_thread.start()
    message_thread.start()
    order_thread.join()
    message_thread.join()
    beautiful_pipeline_end_parallel()
    build_tree_house(refined_part_list)
    send_party_invitations()
    buy_snacks(people_list)

if __name__ == "__main__":
    tree_house_construction_process()
