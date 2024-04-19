from tools.working_station_is import EmptyScan
from tools.working_station_is import ScanOrder
from tools.working_station_is import DisplaysScanningUI
from tools.worker import AssembleParts

import threading

def display_scanning_ui_and_assemble_parts(order_id):
    DisplaysScanningUI.call(order_id=order_id)
    AssembleParts.call()

def process():
    EmptyScan.call()
    order_id = ScanOrder.call()
    beautiful_pipeline_parallel()
    thread_ui = threading.Thread(target=DisplaysScanningUI.call, args=(order_id,))
    thread_assemble = threading.Thread(target=AssembleParts.call)
    thread_ui.start()
    thread_assemble.start()
    thread_ui.join()
    thread_assemble.join()
    beautiful_pipeline_end_parallel()
    return "Process completed."

if __name__ == "__main__":
    result = process()
    print(result)