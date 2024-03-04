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

    # Parallel execution for evaluating parts list and configuring the robotic assembly line
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

    # Coating the brackets for durability enhancement
    EnhanceProduct.call()

    return True

if __name__ == "__main__":
    product_id = 123
    part_list = ["metal_sheet", "bolts", "nuts"]
    process_result = process_order(product_id, part_list)
    if process_result:
        print("Process completed successfully.")
    else:
        print("Process failed or was terminated.")