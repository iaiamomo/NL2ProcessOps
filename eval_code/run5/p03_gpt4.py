from tools.l12 import L12AssembleSpindle
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.smart_tester import TestSpindle
def process_spindle_order(part_list):
    # Retrieve raw materials and set up L12 line in parallel
    materials_retrieved = RetrieveRawMaterials.call(part_list=part_list)
    l12_line_set_up = L12SetUp.call()

    # Proceed only if both materials are retrieved and L12 line is set up
    if materials_retrieved and l12_line_set_up:
        # Assemble the spindle
        spindle_assembled = L12AssembleSpindle.call(part_list=part_list)
        if spindle_assembled:
            # Test the spindle
            test_result = TestSpindle.call(product_id=1)  # Assuming a placeholder product ID
            if not test_result:
                # If test fails, send to maintenance
                print("Spindle failed the test, sending to maintenance.")
            else:
                print("Spindle assembled and passed the test.")
        else:
            print("Failed to assemble the spindle.")
    else:
        print("Failed to retrieve materials or set up L12 line.")

    return spindle_assembled and test_result

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    process_result = process_spindle_order(part_list)
    if process_result:
        print("Process completed successfully.")
    else:
        print("Process failed.")