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
    part_list = GenerateRequirementTreeHouse.call()
    refined_part_list = part_list
    additional_requirements = True  
    while beautiful_pipeline_loop_check(additional_requirements):
        refined_part_list = RefineRequirementsTreeHouse.call(part_list=refined_part_list)
        additional_requirements = False  
    return refined_part_list

def order_materials(part_list):
    OrderParts.call(part_list=part_list)

def message_friends_for_help():
    friends_list = ["Alice", "Bob", "Charlie"]
    SendRequirements.call(part_list=friends_list)

def build_tree_house(part_list):
    AssembleTreeHouse.call(part_list=part_list)

def send_party_invitations():
    people_list = ["Alice", "Bob", "Charlie", "Dana"]
    SendInvitations.call(people=people_list)
    return people_list

def buy_snacks(people_list):
    BuySnacks.call(people=people_list)

def tree_house_construction_process():
    refined_part_list = collect_and_refine_requirements()
    beautiful_pipeline_parallel()
    order_thread = threading.Thread(target=order_materials, args=(refined_part_list,))
    message_thread = threading.Thread(target=message_friends_for_help)
    order_thread.start()
    message_thread.start()
    order_thread.join()
    message_thread.join()
    beautiful_pipeline_end_parallel()
    build_tree_house(refined_part_list)
    people_list = send_party_invitations()
    buy_snacks(people_list)

if __name__ == "__main__":
    tree_house_construction_process()