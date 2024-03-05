from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.welding_machine import AssembleParts
def process_pallet_arrival():
    # Empty the scan results when a pallet arrives at the working station
    EmptyScan.call()
    
    # The worker scans the order and the system returns the order ID
    order_id = ScanOrder.call()
    
    # In parallel, display the scanning UI and the worker assembles the part
    DisplaysScanningUI.call(order_id=order_id)
    AssembleParts.call()

    return "Process completed."

if __name__ == "__main__":
    result = process_pallet_arrival()
    print(result)