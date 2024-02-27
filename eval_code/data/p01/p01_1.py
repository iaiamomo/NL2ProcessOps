from threading import Thread
from tools.working_station_is import EmptyScan, ScanOrder, DisplaysScanningUI
from tools.worker import AssembleParts
from tools.pallet import PalletArrives

def displayscanningui(order_id):
    DisplaysScanningUI.call(order_id)

def assembleparts():
    AssembleParts.call()

def process():
    PalletArrives.call()

    EmptyScan.call()

    order_id = ScanOrder.call()

    thread_display = Thread(target=displayscanningui, args=(order_id))
    thread_assemble = Thread(target=assembleparts, args=())
    thread_display.start()
    thread_assemble.start()
    thread_display.join()
    thread_assemble.join()


if __name__ == "__main__":
    process()