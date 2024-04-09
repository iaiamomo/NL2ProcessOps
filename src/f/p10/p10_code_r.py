import threading
def process_part_list(part_list):
    for part in part_list:
        part_available = True  
        if check(part_available):
            pass  
        else:
            pass  
def prepare_for_assembling():
    pass
def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if check(order_accepted):
        InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
        threads = []
        thread_storehouse = threading.Thread(target=process_part_list, args=(part_list,))
        thread_engineering = threading.Thread(target=prepare_for_assembling)
        threads.append(thread_storehouse)
        threads.append(thread_engineering)
        parallel()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        end_parallel()
        AssembleBicycle.call(part_list=part_list)
        print("Bicycle shipped to customer")
    else:
        print("Order rejected")
if __name__ == "__main__":
    process_order()