from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.wms_is import RetrieveRawMaterials
from tools.manufacturer import OrderParts
from tools.manufacturer import SendMessage
from tools.manufacturer import SendInvitations
from tools.manufacturer import CreateListOfPeople
import threading

def collect_and_refine_requirements():
    part_list = GenerateRequirementTreeHouse.call()
    refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
    while part_list != refined_part_list:
        part_list = refined_part_list
        refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
    return refined_part_list

def order_materials(part_list):
    OrderParts.call(part_list=part_list)

def send_messages_to_friends():
    SendMessage.call(message="Help me build a tree house!")

def build_tree_house(part_list):
    AssembleTreeHouse.call(part_list=part_list)

def send_invitations():
    people_list = CreateListOfPeople.call()
    SendInvitations.call(people=people_list)

def process():
    refined_part_list = collect_and_refine_requirements()
    
    # Parallel execution for ordering materials and sending messages to friends
    order_thread = threading.Thread(target=order_materials, args=(refined_part_list,))
    message_thread = threading.Thread(target=send_messages_to_friends)
    
    order_thread.start()
    message_thread.start()
    
    order_thread.join()
    message_thread.join()
    
    build_tree_house(refined_part_list)
    send_invitations()

if __name__ == "__main__":
    process()