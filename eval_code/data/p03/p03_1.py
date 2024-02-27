from tools.crm_is import ReceiveOrder
from tools.wms_is import RetrieveRawMaterials
from tools.l12 import L12SetUp
from tools.l12 import L12AssembleSpindle
from tools.smart_tester import TestSpindle
from tools.cmms_is import ProductMaintenance

from threading import Thread

def retrieverawmaterials(part_list):
    RetrieveRawMaterials.call(part_list=part_list)

def l12setup():
    L12SetUp.call()

def process():
    part_list, product_id = ReceiveOrder.call()

    thread_rawmaterials = Thread(target=retrieverawmaterials, args=(part_list))
    thread_l12setup = Thread(target=l12setup, args=())
    thread_rawmaterials.start()
    thread_l12setup.start()
    thread_rawmaterials.join()
    thread_l12setup.join()

    L12AssembleSpindle.call(part_list=part_list)

    passed = TestSpindle.call(product_id=product_id)
    if not passed:
        ProductMaintenance.call()

if __name__ == "__main__":
    process()
