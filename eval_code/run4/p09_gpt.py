from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.wms_is import RetrieveRawMaterials
from tools.manufacturer import OrderParts
from tools.manufacturer import SendMessage
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendInvitations
from tools.manufacturer import CreateListOfPeople
from threading import Thread
import time

# Assuming the tools are already imported and available for use as described

def collect_and_refine_requirements():
    part_list = GenerateRequirementTreeHouse.call()
    refined_part_list = part_list
    while True:
        # Simulate the refinement process with the architect
        refined_part_list = RefineRequirementsTreeHouse.call(part_list=refined_part_list)
        # Assuming a condition to break the loop, for simplicity, we use a dummy condition
        # In a real scenario, this could be user input or a specific change in the requirements
        if len(refined_part_list) == len(part_list):
            break
        part_list = refined_part_list
    return refined_part_list

def order_materials(part_list):
    OrderParts.call(part_list=part_list)

def send_messages_to_friends():
    SendMessage.call(message="We are building a tree house, can you help?")

def build_house(part_list):
    AssembleTreeHouse.call(part_list=part_list)

def send_invitations():
    people_list = CreateListOfPeople.call()
    SendInvitations.call(people=people_list)

def tree_house_process():
    refined_part_list = collect_and_refine_requirements()
    
    # Parallel execution for ordering materials and sending messages to friends
    order_thread = Thread(target=order_materials, args=(refined_part_list,))
    message_thread = Thread(target=send_messages_to_friends)
    
    order_thread.start()
    message_thread.start()
    
    # Wait for both threads to complete
    order_thread.join()
    message_thread.join()
    
    # Continue with the sequential part of the process
    build_house(refined_part_list)
    send_invitations()

if __name__ == "__main__":
    tree_house_process()