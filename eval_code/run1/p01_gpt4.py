from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.worker import AssembleParts
from tools.welding_machine import AssembleParts
import threading

# Assuming the tools are already imported and available for use as described.
# Each tool can be called using <ToolName>.call() with the appropriate parameters.

def display_scanning_ui_and_assemble_part(order_id):
    # Display scanning UI
    DisplaysScanningUI.call(order_id=order_id)
    # Assemble part by worker
    AssembleParts.call()

def process():
    # Empty scan results
    EmptyScan.call()
    
    # Scan order and get order_id
    order_id = ScanOrder.call()
    
    # Start parallel tasks: Display scanning UI and Assemble part
    thread = threading.Thread(target=display_scanning_ui_and_assemble_part, args=(order_id,))
    thread.start()
    # Assemble part by welding machine in parallel
    AssembleParts.call()  # Assuming this is the call for the welding machine as per the description
    thread.join()

    return "Process completed."

if __name__ == "__main__":
    result = process()
    print(result)