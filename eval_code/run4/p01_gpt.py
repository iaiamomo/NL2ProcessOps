from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.worker import AssembleParts
from tools.welding_machine import AssembleParts
from tools.manufacturer import AssembleBicycle
from tools.robot import MoveRobot
import threading

# Assuming the tools are already imported and available for use

def empty_scan_results():
    EmptyScan.call()

def scan_order():
    return ScanOrder.call()

def display_scanning_ui(order_id):
    DisplaysScanningUI.call(order_id=order_id)

def worker_assembles_part():
    AssembleParts.call()

def process():
    # Empty the scan results
    empty_scan_results()
    
    # Scan the order and get the order_id
    order_id = scan_order()
    
    # Display the scanning UI in parallel with worker assembling the part
    display_ui_thread = threading.Thread(target=display_scanning_ui, args=(order_id,))
    assemble_part_thread = threading.Thread(target=worker_assembles_part)
    
    display_ui_thread.start()
    assemble_part_thread.start()
    
    display_ui_thread.join()
    assemble_part_thread.join()

if __name__ == "__main__":
    process()