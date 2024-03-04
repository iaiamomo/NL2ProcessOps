from tools.working_station_is import ScanOrder
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.worker import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import ScanOrder, ConfigureAssemblyLine, CutMetal, AssembleParts, CheckQualityBrackets, EnhanceProduct

def evaluate_parts_lists():
    # This function represents the task of evaluating parts lists.
    # Since there's no specific tool given for this, it's assumed to be a manual or an implicit process.
    pass

def process_order():
    # Scan the order
    order_id = ScanOrder.call()
    
    # Configure the robotic assembly line and evaluate parts lists in parallel
    threads = []
    threads.append(threading.Thread(target=ConfigureAssemblyLine.call))
    threads.append(threading.Thread(target=evaluate_parts_lists))
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    # Cut the metal
    CutMetal.call()
    
    # Assemble parts
    AssembleParts.call()
    
    # Inspect brackets
    quality_ok = CheckQualityBrackets.call()
    
    if not quality_ok:
        return "Process ended due to defective brackets."
    
    # Coating system
    EnhanceProduct.call()
    
    return "Process completed successfully."

if __name__ == "__main__":
    result = process_order()
    print(result)