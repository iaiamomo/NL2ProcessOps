from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.worker import AssembleParts
from tools.welding_machine import AssembleParts
from tools.manufacturer import AssembleBicycle
import threading

# Assuming the tools are already imported and available for use as described.
def process():
    # Step 1: Empty Scan Results
    EmptyScan.call()
    
    # Step 2: Scan Order
    order_id = ScanOrder.call()
    
    # Step 3: Display Scanning UI
    DisplaysScanningUI.call(order_id=order_id)
    
    # Step 4: Parallel execution of Worker Assembles Part and Worker Scans Part
    def worker_assembles_part():
        AssembleParts.call()  # Assuming this is the correct call for "Worker Assembles Part"
    
    def worker_scans_part():
        # Assuming there's a missing tool for "Worker Scans Part", so we simulate it
        pass  # Simulate the scanning part action by the worker
    
    assemble_thread = threading.Thread(target=worker_assembles_part)
    scan_thread = threading.Thread(target=worker_scans_part)
    
    assemble_thread.start()
    scan_thread.start()
    
    assemble_thread.join()
    scan_thread.join()
    
    # Assuming the process ends after the parallel tasks
    print("Process completed.")

if __name__ == "__main__":
    process()