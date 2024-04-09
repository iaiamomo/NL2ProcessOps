from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import EmptyScan, ScanOrder, DisplaysScanningUI, AssembleParts

def display_scanning_ui_and_assemble_parts(order_id):
    # Display scanning UI and assemble parts in parallel
    def display_ui():
        DisplaysScanningUI.call(order_id=order_id)
    
    def assemble_parts():
        AssembleParts.call()
    
    # Start parallel execution
    parallel()
    ui_thread = Thread(target=display_ui)
    assemble_thread = Thread(target=assemble_parts)
    ui_thread.start()
    assemble_thread.start()
    ui_thread.join()
    assemble_thread.join()
    # End parallel execution
    end_parallel()

def process_pallet():
    # Empty scan results
    EmptyScan.call()
    
    # Scan order and get order_id
    order_id = ScanOrder.call()
    
    # Display scanning UI and assemble parts in parallel
    display_scanning_ui_and_assemble_parts(order_id)

    return "Process completed"

if __name__ == "__main__":
    result = process_pallet()
    print(result)