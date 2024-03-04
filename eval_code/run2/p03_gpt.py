from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
import threading

# Assuming the tools are already imported and available for use as described
def process(part_list, product_id):
    # Retrieve raw materials and set up L12 line in parallel
    def retrieve_raw_materials():
        return RetrieveRawMaterials.call(part_list=part_list)

    def setup_l12_line():
        return L12SetUp.call()

    thread1 = threading.Thread(target=retrieve_raw_materials)
    thread2 = threading.Thread(target=setup_l12_line)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    # Once both tasks are done, proceed with the assembly
    assembly_result = L12AssembleSpindle.call(part_list=part_list)
    if not assembly_result['assembled']:
        return False

    # Test and run-in the spindle
    test_result = TestSpindle.call(product_id=product_id)
    if not test_result['passed']:
        # If test outcome is negative, send spindle to maintenance
        # Assuming sending to maintenance doesn't affect the outcome for simplicity
        return False

    # If everything goes well, the process ends successfully
    return True

if __name__ == "__main__":
    part_list = ['part1', 'part2', 'part3']  # Example part list
    product_id = 123  # Example product ID
    process_result = process(part_list, product_id)
    print(f"Process completed successfully: {process_result}")