from tools.crm_is import ReceiveOrder
from tools.wms_is import RetrieveRawMaterials
from tools.assembly_line import ConfigureAssemblyLine
from tools.precision_machine import CutMetal
from tools.welding_machine import AssembleParts
from tools.vision_is import CheckQualityBrackets
from tools.coating_machine import EnhanceProduct

from threading import Thread

def configureassemblyline():
    ConfigureAssemblyLine.call()

def retrieverawmaterials(part_list):
    RetrieveRawMaterials.call(part_list)

def process():
    part_list, product_id = ReceiveOrder.call()

    thread_1 = Thread(target=retrieverawmaterials, args=(part_list,))
    thread_2 = Thread(target=configureassemblyline)
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()

    CutMetal.call()

    AssembleParts.call()

    defects = CheckQualityBrackets.call()

    if not defects:
        EnhanceProduct.call()

if __name__ == "__main__":
    process()