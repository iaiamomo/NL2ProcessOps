from tools.crm_is import AcceptOrder
from tools.manufacturer import SendRequirements
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.welding_machine import AssembleParts
from tools.worker import AssembleParts
from tools.manufacturer import AssembleBicycle
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import AcceptOrder, SendRequirements, ConfigureAssemblyLine, CutMetal, AssembleParts, CheckQualityBrackets, EnhanceProduct

def process_order(product_id, part_list):
    # Accept the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order not accepted."

    # Parallel execution for evaluating parts lists and configuring the robotic assembly line
    def evaluate_parts_lists():
        SendRequirements.call(part_list=part_list)

    def configure_robotic_assembly_line():
        ConfigureAssemblyLine.call()

    thread1 = threading.Thread(target=evaluate_parts_lists)
    thread2 = threading.Thread(target=configure_robotic_assembly_line)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    # Sequential tasks for cutting metal, assembling parts, and inspecting brackets
    CutMetal.call()
    AssembleParts.call()

    quality_ok = CheckQualityBrackets.call()
    if not quality_ok:
        return "Process ended due to defective brackets."

    # Apply coating if brackets are not defective
    EnhanceProduct.call()

    return "Process completed successfully."

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['part1', 'part2', 'part3']  # Example parts list
    result = process_order(product_id, part_list)
    print(result)