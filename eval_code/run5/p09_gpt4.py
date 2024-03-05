from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import SendInvitations
from tools.manufacturer import BuySnacks
def collect_requirements():
    return GenerateRequirementTreeHouse.call()

def refine_requirements(initial_requirements):
    refined_requirements = RefineRequirementsTreeHouse.call(part_list=initial_requirements)
    return refined_requirements

def send_requirements_to_architect(requirements):
    SendRequirementsArchitect.call(part_list=requirements)

def create_material_list(final_requirements):
    # Assuming the final requirements include the material list
    return final_requirements

def order_materials(material_list):
    OrderParts.call(part_list=material_list)

def send_build_requests(material_list):
    SendRequirements.call(part_list=material_list)

def assemble_tree_house(material_list):
    AssembleTreeHouse.call(part_list=material_list)

def send_party_invitations(friends_list):
    SendInvitations.call(people=friends_list)

def buy_party_snacks(attendees_list):
    BuySnacks.call(people=attendees_list)

def tree_house_building_process():
    initial_requirements = collect_requirements()
    refined_requirements = refine_requirements(initial_requirements)
    send_requirements_to_architect(refined_requirements)
    material_list = create_material_list(refined_requirements)
    order_materials(material_list)
    send_build_requests(material_list)
    assemble_tree_house(material_list)
    friends_list = ["Alice", "Bob", "Charlie"]  # Example friends list
    send_party_invitations(friends_list)
    attendees_list = ["Alice", "Charlie"]  # Example attendees list, assuming some confirmations
    buy_party_snacks(attendees_list)
    print("Tree house built and party organized successfully!")

if __name__ == "__main__":
    tree_house_building_process()