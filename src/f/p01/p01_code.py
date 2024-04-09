import threading

# Assuming the tools are already imported as per the guidelines
# from tools import EmptyScan, ScanOrder, DisplaysScanningUI, AssembleParts

def empty_scan_and_scan_order():
    # Empty the scan results
    EmptyScan.call()
    # Scan the order and get the order_id
    order_id = ScanOrder.call()
    return order_id

def display_scanning_ui(order_id):
    # Display the scanning UI
    DisplaysScanningUI.call(order_id=order_id)

def assemble_part():
    # Assemble the part
    AssembleParts.call()

def process():
    # Start the process by emptying scan results and scanning the order
    order_id = empty_scan_and_scan_order()
    
    # Create threads for parallel execution of displaying scanning UI and assembling part
    thread_ui = threading.Thread(target=display_scanning_ui, args=(order_id,))
    thread_assemble = threading.Thread(target=assemble_part)
    
    # Start the threads
    thread_ui.start()
    thread_assemble.start()
    
    # Wait for both threads to complete
    thread_ui.join()
    thread_assemble.join()
    
    # Process ends
    print("Process completed.")

if __name__ == "__main__":
    process()