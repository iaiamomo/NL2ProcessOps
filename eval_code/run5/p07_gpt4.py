from tools.crm_is import ReceiveOrder
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import AssembleInterior
from tools.manufacturer import OrderParts
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import AcceptOrder
def process_airplane_order():
    # Receive the order from the customer
    part_list, product_id = ReceiveOrder.call()

    # Inform the storehouse and engineering departments about the new order
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Order the parts needed for the airplane's interior
    OrderParts.call(part_list=part_list)

    # Assemble the interior of the plane
    AssembleInterior.call(part_list=part_list, product_id=product_id)

    # Create the test protocol for the airplane
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)

    # Accept the order and check if it is accepted
    order_accepted = AcceptOrder.call(product_id=product_id)

    # Return the result of the process
    return {
        "product_id": product_id,
        "order_accepted": order_accepted,
        "test_protocol": test_protocol
    }

if __name__ == "__main__":
    result = process_airplane_order()
    print(f"Order for product ID {result['product_id']} has been {'accepted' if result['order_accepted'] else 'rejected'}.")
    print(f"Test Protocol: {result['test_protocol']}")