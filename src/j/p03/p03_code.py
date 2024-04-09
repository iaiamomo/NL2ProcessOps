from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import L12AssembleSpindle, RetrieveRawMaterials, L12SetUp, TestSpindle

def retrieve_and_setup(part_list):
    # Retrieve raw materials
    retrieved = RetrieveRawMaterials.call(part_list=part_list)
    # Set up L12 line
    set_up = L12SetUp.call()
    return retrieved, set_up

def assemble_test_maintenance(part_list, product_id):
    # Assemble spindle
    assembled = L12AssembleSpindle.call(part_list=part_list)
    if assembled:
        # Test and run-in spindle
        test_passed = TestSpindle.call(product_id=product_id)
        if not test_passed:
            # Send to maintenance
            print("Spindle sent to maintenance")
    else:
        print("Assembly failed")

def process(part_list, product_id):
    # Start the process
    print("Process started for product ID:", product_id)
    
    # Parallel execution of retrieving raw materials and setting up L12 line
    parallel()
    t1 = Thread(target=retrieve_and_setup, args=(part_list,))
    t1.start()
    end_parallel()
    
    t1.join()
    retrieved, set_up = t1._result
    
    if retrieved and set_up:
        assemble_test_maintenance(part_list, product_id)
    else:
        print("Process failed due to issues in retrieving materials or setting up the line")
    
    return "Process completed"

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]
    product_id = 123
    result = process(part_list, product_id)
    print(result)