from tools.smart_tester import TestSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.l12 import L12SetUp
from tools.l12 import L12AssembleSpindle
def process_spindle_order(part_list):
    # Retrieve raw materials and set up L12 line in parallel
    materials_retrieved = RetrieveRawMaterials.call(part_list=part_list)
    line_set_up = L12SetUp.call()

    # Check if both tasks were successful
    if materials_retrieved and line_set_up:
        # Assemble the spindle
        spindle_assembled = L12AssembleSpindle.call(part_list=part_list)
        if spindle_assembled:
            # Test the spindle
            test_passed = TestSpindle.call(product_id=1)  # Assuming product_id is known or generated here
            if not test_passed:
                # If test failed, send to maintenance
                print("Spindle sent to maintenance.")
            else:
                print("Spindle assembly and testing successful.")
        else:
            print("Failed to assemble spindle.")
    else:
        print("Failed to retrieve materials or set up L12 line.")

    return materials_retrieved and line_set_up and spindle_assembled and test_passed

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    process_result = process_spindle_order(part_list)
    if process_result:
        print("Process completed successfully.")
    else:
        print("Process failed.")