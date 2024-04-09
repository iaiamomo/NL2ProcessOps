def process_order(product_id, part_list):
    order_accepted = AcceptOrder.call(product_id=product_id)
    if check(order_accepted):
        InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
        parallel()
        # Thread for processing part list
        def process_part_list(part_list):
            for part in part_list:
                # Simulate checking part availability and reserving or back-ordering
                # This part is abstracted as we don't have specific methods for these actions
                pass

        # Thread for preparing for assembling
        def prepare_for_assembling():
            # Simulate preparation steps
            # This part is abstracted as we don't have specific methods for these actions
            pass

        thread1 = threading.Thread(target=process_part_list, args=(part_list,))
        thread2 = threading.Thread(target=prepare_for_assembling)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        end_parallel()

        AssembleBicycle.call(part_list=part_list)
        # Simulate shipping bicycle
        # This part is abstracted as we don't have specific methods for shipping
    else:
        # Order rejected, process ends
        pass

    return "Process Completed"

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['wheel', 'frame', 'pedal']  # Example part list
    result = process_order(product_id, part_list)
    print(result)