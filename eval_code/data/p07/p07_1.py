from tools.crm_is import ReceiveOrder, DeliverProduct, DeliverTestProtocol
from tools.manufacturer import SendRequirements, ReceiveParts, AssembleInterior, CreateTestProtocol

def process():
    part_list, product_id = ReceiveOrder.call()

    SendRequirements.call(part_list)

    ReceiveParts.call()

    AssembleInterior.call(part_list, product_id)

    protocol = CreateTestProtocol.call(part_list, product_id)

    DeliverTestProtocol.call(product_id, protocol)

    DeliverProduct.call(product_id)

if __name__ == '__main__':
    process()