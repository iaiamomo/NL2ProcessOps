from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.worker import AssembleParts
import threading

# Assuming the tools are already imported and available for use as described
# EmptyScan, ScanOrder, DisplaysScanningUI, AssembleParts

def worker_assembles_and_scans():
    # Worker assembles the part
    AssembleParts.call()
    # Worker scans the part after assembling
    # Assuming there's a tool for scanning the part which is not explicitly mentioned
    # This could be a placeholder for the actual scanning action
    print("Worker scans the part after assembling")

def process():
    # Empty the scan results when a pallet arrives
    EmptyScan.call()
    
    # Worker scans the order and gets the order_id
    order_id = ScanOrder.call()
    
    # Display the scanning UI to the worker
    DisplaysScanningUI.call(order_id=order_id)
    
    # Worker assembles the part and scans it in parallel
    # Creating a thread for the assembly and scanning process
    assembly_and_scanning_thread = threading.Thread(target=worker_assembles_and_scans)
    
    # Starting the parallel process
    assembly_and_scanning_thread.start()
    
    # Wait for the assembly and scanning process to complete
    assembly_and_scanning_thread.join()
    
    # Process ends after the part is assembled and scanned
    print("Process completed.")

if __name__ == "__main__":
    process()