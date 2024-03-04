from tools.crm_is import AcceptOrder
from tools.manufacturer import SendRequirements
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.worker import AssembleParts
from tools.vision_is import CheckQualityBrackets
import threading

# Assuming the tools are already imported and available for use as described
def process_order(product_id, part_list):
    # Accept the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order not accepted"

    # Parallel tasks for evaluating parts lists and configuring the robotic assembly line
    def evaluate_parts_lists():
        SendRequirements.call(part_list=part_list)

    def configure_assembly_line():
        ConfigureAssemblyLine.call()

    threads = []
    threads.append(threading.Thread(target=evaluate_parts_lists))
    threads.append(threading.Thread(target=configure_assembly_line))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Sequential tasks for cutting metal, assembling parts, and inspecting brackets
    CutMetal.call()
    AssembleParts.call()
    quality_ok = CheckQualityBrackets.call()

    if not quality_ok:
        return "Process ended due to defective brackets"

    # If no defective brackets, proceed with coating system
    # Assuming there's a tool for the coating system, but it's not listed in the provided tools
    # CoatingSystem.call()

    return "Process completed successfully"

if __name__ == "__main__":
    product_id = 123
    part_list = ["part1", "part2", "part3"]
    result = process_order(product_id, part_list)
    print(result)