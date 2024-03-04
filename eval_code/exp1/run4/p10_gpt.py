from tools.manufacturer import AssembleBicycle
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import OrderParts
from tools.worker import AssembleParts
from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import AcceptOrder, InformStorehouseEngineering, OrderParts, AssembleBicycle

def check_and_order_parts(part_list):
    for part in part_list:
        # Simulating the check for part availability and ordering if not available
        # This is a simplification, in a real scenario, this would involve inventory management
        # For the sake of this exercise, we assume all parts need to be ordered
        OrderParts.call(part_list=[part])

def prepare_and_assemble_bicycle(part_list):
    # Simulating the preparation for assembly, which in a real scenario would involve various tasks
    # For this exercise, we directly call the assembly function after preparation is assumed to be done
    AssembleBicycle.call(part_list=part_list)

def process_order(product_id, part_list):
    order_accepted = AcceptOrder.call(product_id=product_id)
    if order_accepted:
        InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
        
        # Processing parts and preparing for assembly in parallel
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
    product_id = 123  # Example product ID
    part_list = ['wheel', 'frame', 'pedal']  # Example part list
    process_order(product_id, part_list)