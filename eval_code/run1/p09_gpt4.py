from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import BuySnacks
import threading

def collect_requirements_and_send_to_architect():
    part_list = GenerateRequirementTreeHouse.call()
    SendRequirementsArchitect.call(part_list=part_list)
    return part_list

def refine_requirements(part_list):
    refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
    return refined_part_list

def order_materials(part_list):
    OrderParts.call(part_list=part_list)

def message_friends_for_help():
    # Assuming there's a function or a way to message friends which is not detailed in the tools.
    # This is a placeholder for the actual implementation.
    print("Messaging friends for help...")

def build_tree_house(part_list):
    AssembleTreeHouse.call(part_list=part_list)

def send_party_invitations():
    # Assuming there's a function or a way to send party invitations which is not detailed in the tools.
    # This is a placeholder for the actual implementation.
    print("Sending party invitations...")

def create_snack_list():
    # Assuming the list of people attending is obtained from the responses to the invitations.
    # This is a placeholder for the actual implementation.
    people_attending = ["Alice", "Bob", "Charlie"]
    BuySnacks.call(people=people_attending)

def process():
    part_list = collect_requirements_and_send_to_architect()
    while True:
        # Assuming there's a way to check if additional requirements are needed which is not detailed in the tools.
        # This is a placeholder for the actual decision-making process.
        additional_requirements_needed = input("Are additional requirements needed? (yes/no): ")
        if additional_requirements_needed.lower() == 'yes':
            part_list = refine_requirements(part_list)
        else:
            break

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
    process()