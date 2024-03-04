from tools.manufacturer import AssembleBicycle
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import OrderParts
from tools.worker import AssembleParts
from threading import Thread

# Assuming the necessary tools are imported as per the provided JSON descriptions
# AcceptOrder, InformStorehouseEngineering, OrderParts, AssembleBicycle

def check_and_order_parts(part_list):
    # This function simulates checking each part's availability and ordering if not available
    # For simplicity, we assume all parts need to be back-ordered
    OrderParts.call(part_list=part_list)

def prepare_and_assemble_bicycle(part_list):
    # This function simulates the preparation for assembly and the assembly itself
    # Since there's no specific tool for preparation, we directly call the assembly tool
    AssembleBicycle.call(part_list=part_list)

def process_order(product_id, part_list):
    order_accepted = AcceptOrder.call(product_id=product_id)
    if order_accepted:
        InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
        
        # Simulate parallel execution of checking/ordering parts and preparing for assembly
        parts_thread = Thread(target=check_and_order_parts, args=(part_list,))
        assembly_thread = Thread(target=prepare_and_assemble_bicycle, args=(part_list,))
        
        parts_thread.start()
        assembly_thread.start()
        
        parts_thread.join()
        assembly_thread.join()
        
        print("Bicycle assembled and ready to be shipped.")
    else:
        print("Order rejected.")

if __name__ == "__main__":
    # Example inputs
    product_id = 123
    part_list = ['wheel', 'frame', 'pedal']
    
    process_order(product_id, part_list)