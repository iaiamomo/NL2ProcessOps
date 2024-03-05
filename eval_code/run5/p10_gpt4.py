from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle
def process_order():
    # Receive a new order
    part_list, product_id = ReceiveOrder.call()

    # Accept or reject the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order rejected."

    # Inform storehouse and engineering department
    SendRequirements.call(part_list=part_list)

    # Assume a simplified process where the storehouse orders parts if not available
    # and the engineering department prepares for assembly simultaneously
    OrderParts.call(part_list=part_list)

    # Assemble the bicycle
    AssembleBicycle.call(part_list=part_list)

    # Ship the bicycle to the customer
    return "Bicycle assembled and shipped to the customer."

if __name__ == "__main__":
    result = process_order()
    print(result)