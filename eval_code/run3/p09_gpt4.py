from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import GenerateRequirementTreeHouse
from tools.manufacturer import AssembleTreeHouse
from tools.manufacturer import SendRequirementsArchitect
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import SendInvitations
from tools.manufacturer import BuySnacks
import threading

def process():
    # Collect Requirements
    part_list = GenerateRequirementTreeHouse.call()

    # Send Requirements to Architect and Receive Draft from Architect
    SendRequirementsArchitect.call(part_list=part_list)

    # Refine Draft with Additional Requirements
    while True:
        refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
        if refined_part_list == part_list:
            break
        else:
            part_list = refined_part_list

    # Create List of Materials
    # Assuming this step is integrated within the refinement or generation process
    # and the final part_list is used for ordering materials

    # Order Materials Online and Message Friends to Help Build (Parallel Execution)
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

    # Build Tree House
    AssembleTreeHouse.call(part_list=part_list)

    # Send Invitations for Tree House Party
    # Assuming we have a predefined list of friends as attendees
    friends_list = ["Alice", "Bob", "Charlie"]
    SendInvitations.call(people=friends_list)

    # Create Attendee List and Buy Snacks
    # Assuming the attendee list is the same as the friends list
    BuySnacks.call(people=friends_list)

if __name__ == "__main__":
    process()