from tools.manufacturer import GenerateRequirementTreeHouse, SendRequirementsArchitect, RefineRequirementsTreeHouse, OrderParts, SendMessage, SendInvitations, AssembleTreeHouse, BuySnacks, CreateListOfPeople

from threading import Thread

def orderparts(part_list):
    OrderParts.call(part_list)

def sendmessage(message):
    SendMessage.call()


def process():
    part_list = GenerateRequirementTreeHouse.call()

    SendRequirementsArchitect.call(part_list)

    part_list = RefineRequirementsTreeHouse.call(part_list)

    t1 = Thread(target=orderparts, args=(part_list,))
    t2 = Thread(target=sendmessage, args=("I'm building a three house",))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    AssembleTreeHouse.call(part_list)

    people = CreateListOfPeople.call()

    SendInvitations.call(people)

    BuySnacks.call(people)

if __name__ == '__main__':
    process()