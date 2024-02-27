from tools.crm_is import ReceiveOrder
from tools.wms_is import OrderRawMaterial
from tools.l12 import L12AssembleSpindle
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import ReceiveOrder, OrderRawMaterial, L12AssembleSpindle, L12SetUp, TestSpindle

def retrieve_raw_materials(part_list):
    for part in part_list:
        OrderRawMaterial.call(part=part)

def set_up_L12_line():
    return L12SetUp.call()

def assemble_spindle(part_list):
    return L12AssembleSpindle.call(part_list=part_list)

def test_spindle(product_id):
    return TestSpindle.call(product_id=product_id)

def process():
    # Receive order
    part_list, product_id = ReceiveOrder.call()

    # Parallel execution for retrieving raw materials and setting up L12 line
    threads = []
    t1 = threading.Thread(target=retrieve_raw_materials, args=(part_list,))
    t2 = threading.Thread(target=set_up_L12_line)
    threads.append(t1)
    threads.append(t2)
    t1.start()
    t2.start()
    for t in threads:
        t.join()

    # Assemble spindle
    assembled = assemble_spindle(part_list)
    if not assembled:
        return "Error in assembling spindle"

    # Test spindle
    passed = test_spindle(product_id)
    if not passed:
        # Send to maintenance
        print("Spindle sent to maintenance")
        return "Process ended with maintenance"

    return "Process successfully completed"

if __name__ == "__main__":
    result = process()
    print(result)