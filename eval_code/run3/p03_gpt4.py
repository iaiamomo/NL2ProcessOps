from tools.smart_tester import TestSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.l12 import L12AssembleSpindle
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import TestSpindle, RetrieveRawMaterials, OrderRawMaterial, RetrieveRawMaterial, L12SetUp, L12AssembleSpindle

def initiate_spindle_order_process(part_list):
    # Parallel tasks for retrieving raw materials and setting up L12 line
    def retrieve_raw_materials():
        return RetrieveRawMaterials.call(part_list=part_list)

    def setup_l12_line():
        return L12SetUp.call()

    thread_retrieve = threading.Thread(target=retrieve_raw_materials)
    thread_setup = threading.Thread(target=setup_l12_line)

    thread_retrieve.start()
    thread_setup.start()

    thread_retrieve.join()
    raw_materials_retrieved = thread_retrieve._target()
    thread_setup.join()
    l12_line_set_up = thread_setup._target()

    # Proceed only if both tasks are completed successfully
    if raw_materials_retrieved and l12_line_set_up:
        # Assemble spindle over L12 line
        spindle_assembled = L12AssembleSpindle.call(part_list=part_list)
        if spindle_assembled:
            # Test and run-in spindle
            test_result = TestSpindle.call(product_id=1)  # Assuming a product ID for demonstration
            if test_result:
                print("Spindle assembly and testing completed successfully.")
            else:
                # Send to maintenance if test fails
                print("Spindle failed the test and is sent to maintenance.")
        else:
            print("Failed to assemble spindle.")
    else:
        print("Failed to retrieve raw materials or set up L12 line.")

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    initiate_spindle_order_process(part_list)