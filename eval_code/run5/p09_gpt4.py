from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import SendInvitations
from tools.manufacturer import BuySnacks
from tools.manufacturer import CreateListOfPeople
def refine_requirements():
    part_list = GenerateRequirementTreeHouse.call()
    refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
    while part_list != refined_part_list:
        part_list = refined_part_list
        refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
    return refined_part_list

def order_materials_and_assemble(refined_part_list):
    OrderParts.call(part_list=refined_part_list)
    AssembleTreeHouse.call(part_list=refined_part_list)

def organize_party():
    people_list = CreateListOfPeople.call()
    SendInvitations.call(people=people_list)
    BuySnacks.call(people=people_list)

def build_tree_house():
    refined_part_list = refine_requirements()
    order_materials_and_assemble(refined_part_list)
    organize_party()

if __name__ == "__main__":
    build_tree_house()