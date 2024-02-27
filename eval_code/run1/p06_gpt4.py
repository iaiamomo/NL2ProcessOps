from tools.crm_is import AcceptOrder
from tools.wms_is import RetrieveRawMaterials
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.welding_machine import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import AcceptOrder, RetrieveRawMaterials, ConfigureAssemblyLine, CutMetal, AssembleParts, CheckQualityBrackets, EnhanceProduct

def process_order(product_id, part_list):
    # Accept the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order not accepted"

    # Define a function to handle parallel tasks
    def handle_parallel_tasks():
        # Evaluate parts lists and retrieve raw materials
        retrieved = RetrieveRawMaterials.call(part_list=part_list)
        # Configure the robotic assembly line
        ConfigureAssemblyLine.call()
        return retrieved

    # Execute parallel tasks
    thread = threading.Thread(target=handle_parallel_tasks)
    thread.start()
    thread.join()

    # Proceed with the production process
    CutMetal.call()
    AssembleParts.call()

    # Inspect brackets
    quality_ok = CheckQualityBrackets.call()
    if not quality_ok:
        return "Process ended due to defective brackets"

    # Apply coating
    EnhanceProduct.call()

    return "Process completed successfully"

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['part1', 'part2', 'part3']  # Example part list
    result = process_order(product_id, part_list)
    print(result)