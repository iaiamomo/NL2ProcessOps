from tools.crm_is import AcceptOrder
from tools.wms_is import RetrieveRawMaterials
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.welding_machine import AssembleParts
from tools.worker import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import AcceptOrder, RetrieveRawMaterials, ConfigureAssemblyLine, CutMetal, AssembleParts, CheckQualityBrackets, EnhanceProduct

def process_order(product_id, part_list):
    # Accept the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return False

    # Parallel execution for evaluating parts list and configuring the assembly line
    def evaluate_parts():
        global parts_retrieved
        parts_retrieved = RetrieveRawMaterials.call(part_list=part_list)

    def configure_assembly_line():
        ConfigureAssemblyLine.call()

    thread1 = threading.Thread(target=evaluate_parts)
    thread2 = threading.Thread(target=configure_assembly_line)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    if not parts_retrieved:
        return False

    # Sequential tasks for cutting metal, assembling brackets, and inspecting them
    CutMetal.call()
    AssembleParts.call()
    quality_ok = CheckQualityBrackets.call()

    if not quality_ok:
        return False

    # Apply coating if the brackets pass the quality inspection
    EnhanceProduct.call()

    return True

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['part1', 'part2', 'part3']  # Example part list
    process_completed = process_order(product_id, part_list)
    if process_completed:
        print("Process completed successfully.")
    else:
        print("Process terminated due to an error or quality issue.")