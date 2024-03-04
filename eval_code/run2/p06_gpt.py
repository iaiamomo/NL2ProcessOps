from tools.working_station_is import ScanOrder
from tools.wms_is import RetrieveRawMaterials
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.worker import AssembleParts
from tools.welding_machine import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct
import threading

# Assuming the tools are already imported and available for use as described
def process_order():
    # Scan the order to get the order ID
    order_id = ScanOrder.call()

    # Configure the assembly line and evaluate parts lists in parallel
    def configure_assembly_line():
        ConfigureAssemblyLine.call()

    def evaluate_and_retrieve_parts():
        # Assuming a predefined parts list for simplicity
        part_list = ["part1", "part2", "part3"]
        retrieved = RetrieveRawMaterials.call(part_list=part_list)
        return retrieved

    thread1 = threading.Thread(target=configure_assembly_line)
    thread2 = threading.Thread(target=evaluate_and_retrieve_parts)

    thread1.start()
    thread2.start()

    thread1.join()
    retrieved = thread2.join()

    if not retrieved:
        print("Failed to retrieve all parts. Ending process.")
        return False

    # Proceed with the metal cutting and assembly
    CutMetal.call()
    AssembleParts.call()  # Assuming this refers to the welding machine's task

    # Inspect the quality of the brackets
    quality_ok = CheckQualityBrackets.call()

    if not quality_ok:
        print("Defective brackets detected. Ending process.")
        return False

    # If brackets are of good quality, proceed with coating
    EnhanceProduct.call()

    print("Process completed successfully.")
    return True

if __name__ == "__main__":
    process_result = process_order()
    if process_result:
        print("The production process completed successfully.")
    else:
        print("The production process was terminated due to an issue.")