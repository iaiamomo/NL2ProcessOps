from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.worker import AssembleParts

import threading

# Assuming the tools are already imported and available for use as described.
# EmptyScan, ScanOrder, DisplaysScanningUI, AssembleParts

def display_scanning_ui_and_assemble_parts(order_id):
    # Display scanning UI
    DisplaysScanningUI.call(order_id=order_id)
    # Assemble parts in parallel
    AssembleParts.call()

def process():
    # Empty scan results
    EmptyScan.call()
    
    # Scan order
    order_id = ScanOrder.call()
    
    # Create threads for parallel execution of displaying scanning UI and assembling parts
    thread_ui = threading.Thread(target=DisplaysScanningUI.call, args=(order_id,))
    thread_assemble = threading.Thread(target=AssembleParts.call)
    
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