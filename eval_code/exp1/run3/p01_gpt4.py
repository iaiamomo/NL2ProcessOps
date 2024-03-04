from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
import threading

# Assuming the tools are already imported and available for use as described
# EmptyScan, ScanOrder, DisplaysScanningUI

def display_scanning_ui_and_assemble_part(order_id):
    # Display the scanning UI
    DisplaysScanningUI.call(order_id=order_id)
    # Simulate assembling part in parallel (not explicitly defined, so no actual function call here)
    # In a real scenario, this could involve calling another tool or performing some operations

def process():
    # Empty the scan results
    EmptyScan.call()
    
    # Scan the order and get the order ID
    order_id = ScanOrder.call()
    
    # Create threads for parallel execution of displaying scanning UI and assembling part
    thread_ui = threading.Thread(target=display_scanning_ui_and_assemble_part, args=(order_id,))
    thread_assemble = threading.Thread(target=lambda: None)  # Placeholder for assembling part, assuming no specific function call is needed
    
    # Start threads
    thread_ui.start()
    thread_assemble.start()
    
    # Wait for both threads to complete
    thread_ui.join()
    thread_assemble.join()
    
    return "Process completed."

if __name__ == "__main__":
    result = process()
    print(result)