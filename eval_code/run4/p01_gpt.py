from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.worker import AssembleParts
import threading

# Assuming the tools are already imported and available for use as described
def process_pallet_arrival():
    # Empty the scan results
    EmptyScan.call()
    
    # Scan the order and get the order_id
    order_id = ScanOrder.call()
    
    # Display the scanning UI
    DisplaysScanningUI.call(order_id=order_id)
    
    # Assemble parts in parallel with another task (not specified)
    def assemble_parts():
        AssembleParts.call()
    
    def another_task():
        # Placeholder for another task that runs in parallel
        pass
    
    # Create threads for parallel execution
    thread_assemble_parts = threading.Thread(target=assemble_parts)
    thread_another_task = threading.Thread(target=another_task)
    
    # Start threads
    thread_assemble_parts.start()
    thread_another_task.start()
    
    # Wait for both threads to complete
    thread_assemble_parts.join()
    thread_another_task.join()
    
    return "Process completed."

if __name__ == "__main__":
    result = process_pallet_arrival()
    print(result)