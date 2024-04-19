from tools.crm_is import AcceptOrder
from tools.wms_is import RetrieveRawMaterials
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.welding_machine import AssembleParts
from tools.worker import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct

import threading

def process_order(product_id, part_list):
    order_accepted = AcceptOrder.call(product_id=product_id)
    if beautiful_pipeline_check(not order_accepted):
        return "Order not accepted"
    def evaluate_parts():
        global parts_retrieved
        parts_retrieved = RetrieveRawMaterials.call(part_list=part_list)
    def configure_assembly():
        ConfigureAssemblyLine.call()
    beautiful_pipeline_parallel()
    thread1 = threading.Thread(target=evaluate_parts)
    thread2 = threading.Thread(target=configure_assembly)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    beautiful_pipeline_end_parallel()
    if beautiful_pipeline_check(not parts_retrieved):
        return "Failed to retrieve parts"
    CutMetal.call()
    AssembleParts.call()
    quality_ok = CheckQualityBrackets.call()
    if beautiful_pipeline_check(not quality_ok):
        return "Defective brackets detected, process ended"
    EnhanceProduct.call()
    return "Process completed successfully"

if __name__ == "__main__":
    product_id = 123  
    part_list = ['partA', 'partB', 'partC']  
    result = process_order(product_id, part_list)
    print(result)