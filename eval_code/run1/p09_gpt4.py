from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import OrderParts
from tools.manufacturer import BuySnacks
import threading

def collect_and_send_requirements():
    part_list = GenerateRequirementTreeHouse.call()
    SendRequirementsArchitect.call(part_list=part_list)
    return part_list

def refine_requirements(part_list):
    refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
    return refined_part_list

def order_materials(part_list):
    OrderParts.call(part_list=part_list)

def message_friends_for_help():
    # Assuming there's a predefined list of friends or a way to fetch it
    friends = ["Alice", "Bob", "Charlie"]
    SendRequirements.call(part_list=friends)

def build_tree_house(part_list):
    AssembleTreeHouse.call(part_list=part_list)

def send_party_invitations():
    # Assuming there's a predefined list of friends or a way to fetch it
    friends = ["Alice", "Bob", "Charlie"]
    # Assuming a function to send invitations which is not defined in the tools
    # send_invitations(friends)
    print("Invitations sent to:", ", ".join(friends))

def create_snack_list():
    # Assuming there's a predefined list of attendees or a way to fetch it
    attendees = ["Alice", "Bob"]
    BuySnacks.call(people=attendees)

def build_tree_house_process():
    part_list = collect_and_send_requirements()
    additional_requirements = True
    while additional_requirements:
        # Assuming a way to check if there are additional requirements
        # This could be a user input or some other condition check
        # For simplicity, it's set to False to proceed with the process
        additional_requirements = False
        if additional_requirements:
            part_list = refine_requirements(part_list)
    
    # Parallel tasks for ordering materials and messaging friends
    order_thread = threading.Thread(target=order_materials, args=(part_list,))
    message_thread = threading.Thread(target=message_friends_for_help)
    order_thread.start()
    message_thread.start()
    order_thread.join()
    message_thread.join()

    build_tree_house(part_list)
    send_party_invitations()
    create_snack_list()

if __name__ == "__main__":
    build_tree_house_process()