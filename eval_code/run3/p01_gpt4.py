from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
import threading

# Assuming the tools are already imported as per the guidelines
# from tools import EmptyScan, ScanOrder, DisplaysScanningUI

def display_scanning_ui_and_assemble_part(order_id):
    DisplaysScanningUI.call(order_id=order_id)
    # Assuming there's a placeholder function for assembling the part since it's not provided as a tool
    assemble_part()

def assemble_part():
    # Placeholder function to represent the assembly part task
    # In a real scenario, this would involve specific actions to assemble the part
    print("Assembling the part...")

def process_pallet():
    # Empty the scan results
    EmptyScan.call()
    
    # Scan the order and get the order_id
    order_id = ScanOrder.call()
    
    # Display scanning UI and assemble part in parallel
    threading.Thread(target=display_scanning_ui_and_assemble_part, args=(order_id,)).start()
    threading.Thread(target=assemble_part).start()

if __name__ == "__main__":
    process_pallet()