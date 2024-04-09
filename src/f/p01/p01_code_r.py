import threading
def empty_scan_and_scan_order():
    EmptyScan.call()
    order_id = ScanOrder.call()
    return order_id
def display_scanning_ui(order_id):
    DisplaysScanningUI.call(order_id=order_id)
def assemble_part():
    AssembleParts.call()
def process():
    order_id = empty_scan_and_scan_order()
    parallel()
    thread_ui = threading.Thread(target=display_scanning_ui, args=(order_id,))
    thread_assemble = threading.Thread(target=assemble_part)
    thread_ui.start()
    thread_assemble.start()
    thread_ui.join()
    thread_assemble.join()
    end_parallel()
    print("Process completed.")
if __name__ == "__main__":
    process()