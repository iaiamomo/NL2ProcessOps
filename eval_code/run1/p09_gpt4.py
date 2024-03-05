from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import BuySnacks
import threading

def collect_requirements():
    return GenerateRequirementTreeHouse.call()

def refine_requirements(part_list):
    return RefineRequirementsTreeHouse.call(part_list=part_list)

def send_requirements_to_architect(part_list):
    SendRequirementsArchitect.call(part_list=part_list)

def order_materials(part_list):
    OrderParts.call(part_list=part_list)

def send_messages_to_friends():
    # Assuming there's a predefined list of friends
    friends = ["Alice", "Bob", "Charlie"]
    SendRequirements.call(part_list=friends)

def build_tree_house(part_list):
    AssembleTreeHouse.call(part_list=part_list)

def send_invitations():
    # Assuming there's a predefined list of friends
    friends = ["Alice", "Bob", "Charlie"]
    # Sending invitations to the same friends who helped build the tree house
    SendRequirements.call(part_list=friends)

def create_list_for_party_snacks():
    # Assuming there's a predefined list of friends who confirmed their attendance
    attending_friends = ["Alice", "Bob"]
    BuySnacks.call(people=attending_friends)

def process():
    part_list = collect_requirements()
    refined_part_list = part_list
    additional_requirements = True

    while additional_requirements:
        send_requirements_to_architect(refined_part_list)
        # Simulate receiving a draft and deciding if more refinement is needed
        # For simplicity, we assume there's a condition that eventually becomes False
        additional_requirements = False  # This would be determined by some logic
        if additional_requirements:
            refined_part_list = refine_requirements(refined_part_list)

    # Once no additional requirements, create list of materials
    final_part_list = refined_part_list

    # Ordering materials and sending messages to friends in parallel
    order_thread = threading.Thread(target=order_materials, args=(final_part_list,))
    message_thread = threading.Thread(target=send_messages_to_friends)
    order_thread.start()
    message_thread.start()
    order_thread.join()
    message_thread.join()

    # Building the tree house
    build_tree_house(final_part_list)

    # Sending invitations for the tree house party
    send_invitations()

    # Creating list for party snacks
    create_list_for_party_snacks()

if __name__ == "__main__":
    process()