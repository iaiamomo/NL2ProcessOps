from tools.crm_is import ReceiveOrder
from tools.manufacturer import AssembleInterior
from tools.manufacturer import OrderParts
from tools.manufacturer import CreateTestProtocol
from tools.crm_is import AcceptOrder
import threading

# Assuming the tools are already imported and available for use as described.
def manufacture_parts(part_list):
    # This function simulates the manufacturing of parts in parallel.
    # Each part could potentially be manufactured by a different team.
    threads = []
    for part in part_list:
        # For simplicity, we're not differentiating between different parts and teams.
        # In a real scenario, you would dispatch to different teams based on the part.
        thread = threading.Thread(target=OrderParts.call, args=([part],))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def process_airplane_order():
    # Receive airplane customization specifications
    part_list, product_id = ReceiveOrder.call()
    
    # Manufacture parts in parallel
    manufacture_parts(part_list)
    
    # Assemble the interior
    AssembleInterior.call(part_list=part_list, product_id=product_id)
    
    # Test flight and create protocol
    test_protocol = CreateTestProtocol.call(part_list=part_list, product_id=product_id)
    
    # Deliver plane to customer and wait for confirmation
    order_accepted = AcceptOrder.call(product_id=product_id)
    if order_accepted:
        print(f"Plane with product ID {product_id} successfully delivered and accepted by the customer.")
    else:
        print(f"Plane with product ID {product_id} delivery or acceptance failed.")

if __name__ == "__main__":
    process_airplane_order()