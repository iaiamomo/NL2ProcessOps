from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.wms_is import RetrieveRawMaterials
from tools.manufacturer import OrderParts
from tools.manufacturer import SendMessage
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendInvitations
from tools.manufacturer import CreateListOfPeople
import threading

def collect_and_refine_requirements():
    part_list = GenerateRequirementTreeHouse.call()
    while True:
        refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
        if refined_part_list == part_list:
            break
        part_list = refined_part_list
    return part_list

def order_materials(part_list):
    OrderParts.call(part_list=part_list)

def send_messages_to_friends():
    SendMessage.call(message="We are building a tree house, can you help?")

def build_tree_house(part_list):
    AssembleTreeHouse.call(part_list=part_list)

def send_invitations():
    people_list = CreateListOfPeople.call()
    SendInvitations.call(people=people_list)

def tree_house_process():
    part_list = collect_and_refine_requirements()
    SendRequirementsArchitect.call(part_list=part_list)
    
    # Parallel tasks for ordering materials and sending messages to friends
    order_thread = threading.Thread(target=order_materials, args=(part_list,))
    message_thread = threading.Thread(target=send_messages_to_friends)
    
    order_thread.start()
    message_thread.start()
    
    order_thread.join()
    message_thread.join()
    
    build_tree_house(part_list)
    send_invitations()

if __name__ == "__main__":
    tree_house_process()