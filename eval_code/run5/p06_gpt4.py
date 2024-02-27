from tools.crm_is import AcceptOrder
from tools.manufacturer import OrderParts
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.welding_machine import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct
def process_bracket_production(product_id, part_list):
    # Accept the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order not accepted."

    # Order parts and configure assembly line in parallel
    OrderParts.call(part_list=part_list)
    ConfigureAssemblyLine.call()

    # Cut metal and assemble parts into brackets
    CutMetal.call()
    AssembleParts.call()

    # Check the quality of the brackets
    quality_ok = CheckQualityBrackets.call()
    if not quality_ok:
        return "Process ended due to defective brackets."

    # Enhance the product's durability
    EnhanceProduct.call()

    return "Process completed successfully."

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['part1', 'part2', 'part3']  # Example parts list
    result = process_bracket_production(product_id, part_list)
    print(result)