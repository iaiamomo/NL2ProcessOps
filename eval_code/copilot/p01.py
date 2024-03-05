from threading import Thread
from working_station_is import PalletArrives, EmptyScan, ScanOrder, DisplaysScanningUI
from worker import AssembleParts

def process():
    # Pallet arrives at the working station
    PalletArrives.call()

    # The system empties the scan results
    EmptyScan.call()

    # The worker scans the order
    order_id = ScanOrder.call()

    # The system displays the scanning UI to the worker
    ui_thread = Thread(target=DisplaysScanningUI.call, args=(order_id,))
    ui_thread.start()

    # In parallel, the worker assembles the part
    AssembleParts.call()

    # Wait for the UI thread to finish
    ui_thread.join()