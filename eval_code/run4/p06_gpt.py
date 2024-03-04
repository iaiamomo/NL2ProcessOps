from tools.crm_is import AcceptOrder
from tools.manufacturer import SendRequirements
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.worker import AssembleParts
from tools.welding_machine import AssembleParts
from tools.manufacturer import AssembleBicycle
from tools.manufacturer import AssembleInterior
from tools.vision_is import CheckQualityBrackets
import threading

# Assuming the tools are already imported and available for use as described in the problem description.

def process_order(product_id, part_list):
    # Accept the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order not accepted"

    # Parallel execution for evaluating parts lists and configuring the robotic assembly line
    def evaluate_parts():
        SendRequirements.call(part_list=part_list)

    def configure_assembly_line():
        ConfigureAssemblyLine.call()

    evaluate_thread = threading.Thread(target=evaluate_parts)
    configure_thread = threading.Thread(target=configure_assembly_line)

    evaluate_thread.start()
    configure_thread.start()

    evaluate_thread.join()
    configure_thread.join()

    # Sequential tasks for cutting metal, assembling parts, and inspecting brackets
    CutMetal.call()
    AssembleParts.call()  # Assuming this refers to the welding machine assembling parts into brackets

    quality_ok = CheckQualityBrackets.call()
    if not quality_ok:
        return "Process ended due to defective brackets"

    # Coating system for enhancing durability
    # Assuming there's a tool for this, but it's not listed. Placeholder call:
    # CoatingSystem.call()

    return "Process completed successfully"

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ["part1", "part2", "part3"]  # Example parts list
    result = process_order(product_id, part_list)
    print(result)