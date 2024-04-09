from threading import Thread

# Assuming the tools are already imported as per the guidelines

def process():
    # Collect Requirements
    part_list = GenerateRequirementTreeHouse.call()

    # Send to Architect and Receive Draft
    SendRequirementsArchitect.call(part_list=part_list)

    # Refine Draft with Additional Requirements
    while True:
        refined_part_list = RefineRequirementsTreeHouse.call(part_list=part_list)
        if refined_part_list == part_list:
            break
        else:
            part_list = refined_part_list

    # Create Materials List
    # Assuming this step is included in the refinement and finalization of the part list

    # Order Materials Online and Message Friends for Help in parallel
    def order_materials():
        OrderParts.call(part_list=part_list)

    def message_friends():
        SendMessage.call(message="Please help me build the tree house.")

    parallel()
    thread1 = Thread(target=order_materials)
    thread2 = Thread(target=message_friends)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end_parallel()

    # Build Tree House
    AssembleTreeHouse.call(part_list=part_list)

    # Send Party Invitations
    # Assuming we have a predefined list of friends
    friends_list = ["Alice", "Bob", "Charlie"]
    SendInvitations.call(people=friends_list)

    # Create Snack List
    # Assuming the creation of the snack list is done based on the number of attendees
    # and does not require a separate tool invocation
    BuySnacks.call(people=friends_list)

    return "Tree house built and party organized successfully!"

if __name__ == "__main__":
    result = process()
    print(result)