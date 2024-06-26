from tools.crm_is import AcceptOrder
from tools.manufacturer import SendRequirements
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.welding_machine import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct
def process_brackets_production(product_id, part_list):
    # Accept the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order not accepted."

    # Send requirements to the proper teams
    SendRequirements.call(part_list=part_list)

    # Configure the assembly line
    ConfigureAssemblyLine.call()

    # Cut the metal
    CutMetal.call()

    # Assemble the parts into brackets
    AssembleParts.call()

    # Check the quality of the brackets
    quality_ok = CheckQualityBrackets.call()
    if not quality_ok:
        return "Process ended due to quality issues."

    # Enhance the product
    EnhanceProduct.call()

    return "Process completed successfully."

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['part1', 'part2', 'part3']  # Example parts list
    result = process_brackets_production(product_id, part_list)
    print(result)