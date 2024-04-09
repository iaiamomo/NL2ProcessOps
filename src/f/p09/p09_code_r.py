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
def send_messages_to_friends():
    SendMessage.call(message="Help me build the tree house!")
def build_tree_house(part_list):
    AssembleTreeHouse.call(part_list=part_list)
def send_invitations(attendees):
    SendInvitations.call(people=attendees)
def create_list_for_party_snacks(attendees):
    BuySnacks.call(people=attendees)
def process():
    part_list = collect_and_send_requirements()
    while True:
        additional_requirements = input("Are there additional requirements? (yes/no): ")
        if check(additional_requirements.lower() == 'yes'):
            part_list = refine_requirements(part_list)
        else:
            break
    parallel()
    order_thread = threading.Thread(target=order_materials, args=(part_list,))
    message_thread = threading.Thread(target=send_messages_to_friends)
    order_thread.start()
    message_thread.start()
    order_thread.join()
    message_thread.join()
    end_parallel()
    build_tree_house(part_list)
    friends = ["Alice", "Bob", "Charlie"]
    send_invitations(friends)
    create_list_for_party_snacks(friends)
if __name__ == "__main__":
    process()