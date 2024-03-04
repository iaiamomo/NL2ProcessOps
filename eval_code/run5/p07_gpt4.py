from tools.crm_is import ReceiveOrder
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import AssembleInterior
from tools.manufacturer import AssembleTreeHouse
from tools.smart_tester import TestSpindle
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import DeliverProduct
from tools.crm_is import AcceptOrder
def process_airplane_order():
    # Receive the order from the customer
    part_list, product_id = ReceiveOrder.call()

    # Inform the storehouse and engineering departments about the new order
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Assemble the interior of the plane
    AssembleInterior.call(part_list=part_list, product_id=product_id)

    # Test the assembled plane
    test_passed = TestSpindle.call(product_id=product_id)

    # If the test is passed, proceed with creating the test protocol and delivering the product
    if test_passed:
        test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
        DeliverProduct.call(product_id=product_id)
        print(f"Test Protocol: {test_protocol}")
        print("Product delivered successfully.")
    else:
        print("Test failed. Please review the assembly process.")

def main():
    # Process an airplane order
    process_airplane_order()

if __name__ == "__main__":
    main()