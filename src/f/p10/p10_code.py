import threading

# Assuming the tools are already imported and available for use as described

def process_part_list(part_list):
    for part in part_list:
        # Simulate checking if part is available and either reserving or back-ordering it
        # This is a simplification, as the actual logic for checking availability and reserving/back-ordering is not provided
        # In a real scenario, this would involve database queries or API calls
        part_available = True  # Placeholder for actual availability check
        if part_available:
            # Reserve part
            pass  # Placeholder for actual reservation logic
        else:
            # Back-order part
            pass  # Placeholder for actual back-order logic

def prepare_for_assembling():
    # Placeholder for actual preparation logic
    pass

def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    
    if order_accepted:
        InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
        
        # Parallel execution for processing part list and preparing for assembling
        threads = []
        thread_storehouse = threading.Thread(target=process_part_list, args=(part_list,))
        thread_engineering = threading.Thread(target=prepare_for_assembling)
        
        threads.append(thread_storehouse)
        threads.append(thread_engineering)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Assuming all parts are successfully reserved or back-ordered and preparation is finished
        AssembleBicycle.call(part_list=part_list)
        # Placeholder for shipping logic
        print("Bicycle shipped to customer")
    else:
        print("Order rejected")

if __name__ == "__main__":
    process_order()