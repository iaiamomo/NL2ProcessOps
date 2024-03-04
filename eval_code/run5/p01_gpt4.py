from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
def process_pallet_arrival():
    # Empty the scan results when a pallet arrives
    EmptyScan.call()
    
    # Worker scans the order and gets the order ID
    order_id = ScanOrder.call()
    
    # Display the scanning UI to the worker with the scanned order ID
    DisplaysScanningUI.call(order_id=order_id)
    
    # In parallel, the worker assembles the part
    # Note: The actual assembly process is not detailed in the tools provided.
    # Assuming a placeholder function for the assembly process
    assemble_part()

def assemble_part():
    # Placeholder function to represent the part assembly by the worker
    print("Assembling the part...")

if __name__ == "__main__":
    process_pallet_arrival()