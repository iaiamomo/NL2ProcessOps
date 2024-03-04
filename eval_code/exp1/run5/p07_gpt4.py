from tools.manufacturer import AssembleInterior
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import DeliverProduct
from tools.crm_is import ReceiveOrder
class AirplaneCustomizationProcess:
    @staticmethod
    def receive_order():
        part_list, product_id = ReceiveOrder.call()
        return part_list, product_id

    @staticmethod
    def assemble_interior(part_list, product_id):
        AssembleInterior.call(part_list=part_list, product_id=product_id)

    @staticmethod
    def create_test_protocol(part_list, product_id):
        test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
        return test_protocol

    @staticmethod
    def deliver_product(product_id):
        DeliverProduct.call(product_id=product_id)

    @staticmethod
    def process_order():
        # Receive the order from the customer
        part_list, product_id = AirplaneCustomizationProcess.receive_order()

        # Assemble the interior based on the received parts list
        AirplaneCustomizationProcess.assemble_interior(part_list, product_id)

        # Create a test protocol for the assembled plane
        test_protocol = AirplaneCustomizationProcess.create_test_protocol(part_list, product_id)

        # Deliver the product to the customer
        AirplaneCustomizationProcess.deliver_product(product_id)

        # Return the test protocol to the caller for verification
        return test_protocol

if __name__ == "__main__":
    # Process an order
    test_protocol = AirplaneCustomizationProcess.process_order()
    print(f"Test Protocol: {test_protocol}")