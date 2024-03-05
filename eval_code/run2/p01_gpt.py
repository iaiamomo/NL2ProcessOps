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

def another_task():
    # Assuming another task is similar to assembling parts but done by a different actor
    # For demonstration, let's assume it's the welding machine assembling parts
    AssembleParts.call()

def process():
    # Empty the scan results
    empty_scan_results()
    
    # Scan the order and get order_id
    order_id = scan_order()
    
    # Display the scanning UI
    display_scanning_ui(order_id)
    
    # Start parallel tasks
    worker_thread = threading.Thread(target=worker_assembles_part)
    another_task_thread = threading.Thread(target=another_task)
    
    worker_thread.start()
    another_task_thread.start()
    
    # Wait for both threads to complete
    worker_thread.join()
    another_task_thread.join()

if __name__ == "__main__":
    process()