from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
import threading

# Assuming the tools are already imported and available for use as described
# EmptyScan, ScanOrder, DisplaysScanningUI

def display_scanning_ui_and_assemble_part(order_id):
    # Display scanning UI
    DisplaysScanningUI.call(order_id=order_id)
    # Simulate assembling part in parallel (no specific tool/method provided for this, so it's just a placeholder)
    print("Assembling part...")

def process():
    # Empty scan results
    EmptyScan.call()
    
    # Scan order
    order_id = ScanOrder.call()
    
    # Create a thread for displaying scanning UI and assembling part in parallel
    thread = threading.Thread(target=display_scanning_ui_and_assemble_part, args=(order_id,))
    thread.start()
    
    # Wait for the thread to complete
    thread.join()
    
    return "Process completed."

if __name__ == "__main__":
    result = process()
    print(result)