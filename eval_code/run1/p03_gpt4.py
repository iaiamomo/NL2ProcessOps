from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
import threading

# Assuming the tools are already imported and available for use as described
def process(part_list, product_id):
    # Step 1: Retrieve raw materials and set up L12 line in parallel
    def retrieve_raw_materials():
        return RetrieveRawMaterials.call(part_list=part_list)

    def setup_l12_line():
        return L12SetUp.call()

    retrieve_thread = threading.Thread(target=retrieve_raw_materials)
    setup_thread = threading.Thread(target=setup_l12_line)

    retrieve_thread.start()
    setup_thread.start()

    retrieve_thread.join()
    setup_thread.join()

    # Both tasks completed, proceed to assemble spindle
    assembly_result = L12AssembleSpindle.call(part_list=part_list)

    if not assembly_result['assembled']:
        return False  # Assembly failed, end process

    # Test and run-in spindle
    test_result = TestSpindle.call(product_id=product_id)

    if not test_result['passed']:
        # Test failed, send to maintenance
        # Assuming maintenance does not affect the outcome of the process
        return True  # Process ends after maintenance

    return True  # Process successfully completed

if __name__ == "__main__":
    part_list = ['part1', 'part2', 'part3']  # Example part list
    product_id = 123  # Example product ID
    process_completed = process(part_list, product_id)
    print(f"Process completed: {process_completed}")