from l12 import L12SetUp, L12AssembleSpindle
from smart_tester import TestSpindle
from wms_is import RetrieveRawMaterials
from cmms_is import ProductMaintenance

def manufacture_spindle(part_list):
    # Retrieve raw materials
    retrieved = RetrieveRawMaterials.call(part_list)
    # Set up the L12 line
    set_up = L12SetUp.call()

    # Wait for both the raw materials to be retrieved and the L12 line to be set up
    if retrieved and set_up:
        # Assemble the spindle
        assembled = L12AssembleSpindle.call(part_list)
        if assembled:
            # Test the spindle
            passed = TestSpindle.call(assembled)
            if not passed:
                # If the test failed, send the spindle to maintenance
                ProductMaintenance.call(assembled)
    else:
        print("Failed to retrieve raw materials or set up the L12 line.")