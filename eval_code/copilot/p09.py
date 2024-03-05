from manufacturer import GenerateRequirementTreeHouse, RefineRequirementsTreeHouse, SendRequirementsArchitect, OrderParts, SendMessage, AssembleTreeHouse, CreateListOfPeople, SendInvitations, BuySnacks

def build_tree_house():
    # Generate requirements
    generate_req = GenerateRequirementTreeHouse()
    part_list = generate_req.call()

    # Send requirements to architect
    send_req_architect = SendRequirementsArchitect()
    send_req_architect.call(part_list)

    # Refine requirements
    refine_req = RefineRequirementsTreeHouse()
    refined_part_list = refine_req.call(part_list)

    # Order parts
    order_parts = OrderParts()
    order_parts.call(refined_part_list)

    # Send messages to friends to build the house
    send_message = SendMessage()
    send_message.call()

    # Assemble tree house
    assemble_tree_house = AssembleTreeHouse()
    assemble_tree_house.call(refined_part_list)

    # Create list of people for the party
    create_list_of_people = CreateListOfPeople()
    people = create_list_of_people.call()

    # Send invitations
    send_invitations = SendInvitations()
    send_invitations.call(people)

    # Buy snacks
    buy_snacks = BuySnacks()
    buy_snacks.call(people)