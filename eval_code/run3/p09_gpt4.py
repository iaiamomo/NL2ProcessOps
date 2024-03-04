from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import SendInvitations
from tools.manufacturer import BuySnacks
import threading

# Assuming the tools are already imported and available for use

def process():
    # Collect requirements
    part_list = GenerateRequirementTreeHouse.call()

    # Send requirements to architect and receive draft
    SendRequirementsArchitect.call(part_list=part_list)

    # Refine draft with additional requirements if needed
    while True:
        refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
        if refined_part_list == part_list:
            break
        else:
            part_list = refined_part_list

    # Create list of materials from the plan
    # Assuming this step is included in the refinement or another process not explicitly defined here

    # Order materials online and message friends for help in parallel
    def order_materials():
        OrderParts.call(part_list=part_list)

    def message_friends():
        SendRequirements.call(part_list=part_list)

    order_thread = threading.Thread(target=order_materials)
    message_thread = threading.Thread(target=message_friends)

    order_thread.start()
    message_thread.start()

    order_thread.join()
    message_thread.join()

    # Build tree house
    AssembleTreeHouse.call(part_list=part_list)

    # Send party invitations
    # Assuming we have a predefined list of friends as 'friends_list'
    friends_list = ["Alice", "Bob", "Charlie"]
    SendInvitations.call(people=friends_list)

    # Create snack list based on the attendees
    # Assuming the BuySnacks tool is used here to represent creating a snack list
    BuySnacks.call(people=friends_list)

if __name__ == "__main__":
    process()