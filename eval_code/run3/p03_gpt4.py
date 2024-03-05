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

    thread_retrieve = threading.Thread(target=retrieve_raw_materials)
    thread_setup = threading.Thread(target=setup_l12_line)

    thread_retrieve.start()
    thread_setup.start()

    thread_retrieve.join()
    thread_setup.join()

    raw_materials_retrieved = thread_retrieve.result()
    l12_line_setup = thread_setup.result()

    # Step 2: Assemble spindle if raw materials are retrieved and L12 line is set up
    if raw_materials_retrieved and l12_line_setup:
        assembly_result = L12AssembleSpindle.call(part_list=part_list)

        # Step 3: Test and run-in spindle
        if assembly_result:
            test_result = TestSpindle.call(product_id=product_id)

            # Step 4: Send to maintenance if test is negative
            if not test_result:
                # Assuming maintenance does not require a specific tool and is just a process step
                print("Spindle sent to maintenance.")
            else:
                print("Spindle assembly and testing completed successfully.")
        else:
            print("Assembly failed.")
    else:
        print("Failed to retrieve raw materials or set up L12 line.")

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    product_id = 123  # Example product ID
    process(part_list, product_id)