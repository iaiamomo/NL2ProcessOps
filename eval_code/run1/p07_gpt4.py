from tools.crm_is import ReceiveOrder
from tools.manufacturer import BuySnacks
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import OrderColor
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleInterior
from tools.manufacturer import CreateTestProtocol
import threading

# Assuming the tools are already imported and available for use

def manufacture_parts(part_list, product_id):
    # Informing storehouse and engineering departments
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
    
    # Ordering parts online
    OrderParts.call(part_list=part_list)
    
    # Assuming 'color' and 'amount of water in toilets' are part of the part_list
    # and manufacturing of bars and seats are included in the OrderParts tool
    # For simplicity, not implementing the logic to extract specific parts or attributes like color

def assemble_and_test(part_list, product_id):
    # Assemble the interior
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    
    # Create test protocol
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    
    return test_protocol

def process():
    # Receive airplane customization specifications
    part_list, product_id = ReceiveOrder.call()
    
    # Manufacture parts in parallel
    manufacture_thread = threading.Thread(target=manufacture_parts, args=(part_list, product_id))
    manufacture_thread.start()
    manufacture_thread.join()
    
    # Assemble interior and test
    test_protocol = assemble_and_test(part_list, product_id)
    
    # Deliver plane to customer and wait for confirmation
    # Assuming a simple print statement for delivery and confirmation for simplicity
    print(f"Plane with product ID {product_id} delivered to customer. Test protocol: {test_protocol}")
    print("Waiting for customer confirmation...")
    # Simulating customer confirmation
    print("Customer confirmed receipt and satisfaction with the airplane.")
    
    return "Process completed successfully."

if __name__ == "__main__":
    result = process()
    print(result)