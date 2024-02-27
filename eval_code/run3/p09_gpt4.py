from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import SendMessage
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendInvitations
from tools.manufacturer import BuySnacks
from threading import Thread

# Assuming the tools are already imported as per the guidelines

def collect_requirements():
    # This function simulates collecting requirements from the user
    # In a real scenario, this could involve user input or reading from a file
    return ["basic tree house"]

def refine_draft(part_list):
    refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
    return refined_part_list

def create_materials_list(draft):
    # This function simulates creating a materials list from the draft
    # The actual implementation would depend on the draft details
    return ["wood", "nails", "hammer"]

def order_materials(materials_list):
    OrderParts.call(part_list=materials_list)

def message_friends_for_help():
    SendMessage.call(message="Please help me build a tree house this weekend!")

def build_tree_house(materials_list):
    AssembleTreeHouse.call(part_list=materials_list)

def send_party_invitations():
    # Simulating a list of friends
    friends = ["Alice", "Bob", "Charlie"]
    SendInvitations.call(people=friends)
    return friends

def create_snack_list(attendees):
    BuySnacks.call(people=attendees)

def process():
    requirements = collect_requirements()
    SendRequirementsArchitect.call(part_list=requirements)
    draft = ["draft plan"]  # Simulating receiving a draft plan
    additional_requirements = True
    while additional_requirements:
        refined_draft = refine_draft(draft)
        # Simulate decision-making process for additional requirements
        if refined_draft == draft:
            additional_requirements = False
        draft = refined_draft
    
    materials_list = create_materials_list(draft)
    
    # Parallel execution for ordering materials and messaging friends
    order_thread = Thread(target=order_materials, args=(materials_list,))
    message_thread = Thread(target=message_friends_for_help)
    order_thread.start()
    message_thread.start()
    order_thread.join()
    message_thread.join()
    
    build_tree_house(materials_list)
    
    attendees = send_party_invitations()
    create_snack_list(attendees)

if __name__ == "__main__":
    process()