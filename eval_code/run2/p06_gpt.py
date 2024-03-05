from tools.working_station_is import ScanOrder
from tools.wms_is import RetrieveRawMaterials
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.worker import AssembleParts
from tools.welding_machine import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct
import threading

# Assuming the tools are already imported and available for use as described.
def process(part_list):
    # Scan the order and get the order_id
    order_id = ScanOrder.call()

    # Configure the assembly line and evaluate parts list in parallel
    def configure_assembly_line():
        ConfigureAssemblyLine.call()

    def evaluate_and_retrieve_parts():
        retrieved = RetrieveRawMaterials.call(part_list=part_list)
        return retrieved

    thread1 = threading.Thread(target=configure_assembly_line)
    thread2 = threading.Thread(target=evaluate_and_retrieve_parts)

    thread1.start()
    thread2.start()

    thread1.join()
    retrieved = thread2.join()

    if not retrieved:
        return False, "Failed to retrieve all parts."

    # Cut the metal
    CutMetal.call()

    # Assemble the parts
    AssembleParts.call()

    # Inspect the brackets
    quality_ok = CheckQualityBrackets.call()

    if not quality_ok:
        return False, "Defective brackets detected."

    # Enhance the product
    EnhanceProduct.call()

    return True, "Process completed successfully."

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]
    success, message = process(part_list)
    print(f"Process status: {success}, Message: {message}")