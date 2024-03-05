from tools.crm_is import ReceiveOrder
from tools.wms_is import RetrieveRawMaterials
from tools.wms_is import OrderRawMaterial
from tools.wms_is import RetrieveRawMaterial
from tools.l12 import L12SetUp
from tools.l12 import L12AssembleSpindle
from tools.smart_tester import TestSpindle
def process_spindle_order():
    # Receive a new order
    part_list, product_id = ReceiveOrder.call()

    # Initialize variables for parallel tasks
    materials_retrieved = False
    line_set_up = False

    # Retrieve raw materials and set up L12 line in parallel
    materials_retrieved = RetrieveRawMaterials.call(part_list=part_list)
    line_set_up = L12SetUp.call()

    # Check if both tasks are completed
    if materials_retrieved and line_set_up:
        # Assemble the spindle
        assembled = L12AssembleSpindle.call(part_list=part_list)
        if assembled:
            # Test the spindle
            passed = TestSpindle.call(product_id=product_id)
            if not passed:
                # If test failed, send to maintenance
                print(f"Spindle {product_id} failed the test and is sent to maintenance.")
            else:
                print(f"Spindle {product_id} passed the test and is ready for delivery.")
        else:
            print(f"Failed to assemble spindle {product_id}.")
    else:
        print("Failed to retrieve materials or set up the L12 line.")

if __name__ == "__main__":
    process_spindle_order()