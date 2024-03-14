def process_spindle_manufacturing():
    # New order arrives
    part_list = ReceiveOrder.call()

    # Retrieve raw materials and Set up L12 lines in parallel
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(RetrievePartList.call, part_list=part_list),
            executor.submit(L12SetUp.call)
        ]
        for future in as_completed(futures):
            result = future.result()
            if not result['retrieved'] and not result['set_up']:
                raise Exception("Failed to retrieve parts or set up L12 lines")

    # Assemble spindle
    assembled = L12AssembleSpindle.call(part_list=part_list)
    if not assembled['assembled']:
        raise Exception("Failed to assemble spindle")

    # Test and run-in spindle
    test_result = TestSpindle.call(product_id=1)  # Assuming product_id is 1 for demonstration
    if not test_result['passed']:
        # Send to maintenance if test failed
        print("Sending spindle to maintenance")
    else:
        print("Spindle assembly and testing completed successfully")