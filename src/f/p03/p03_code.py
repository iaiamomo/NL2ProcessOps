import threading

# Assuming the tools are already imported as per the guidelines
# from tools import TestSpindle, RetrieveRawMaterials, L12SetUp, L12AssembleSpindle

def initiate_process_instance():
    # This function represents the initiation of a new process instance
    # In a real scenario, this could involve logging, setting up initial variables, etc.
    print("New process instance initiated")

def retrieve_and_setup(part_list):
    # Retrieve raw materials and set up L12 line in parallel
    def retrieve():
        retrieved = RetrieveRawMaterials.call(part_list=part_list)
        return retrieved
    
    def setup():
        set_up = L12SetUp.call()
        return set_up
    
    retrieve_thread = threading.Thread(target=retrieve)
    setup_thread = threading.Thread(target=setup)
    
    retrieve_thread.start()
    setup_thread.start()
    
    retrieve_thread.join()
    setup_thread.join()
    
    # Assuming both tasks need to be successful to proceed
    return True

def assemble_spindle(part_list):
    assembled = L12AssembleSpindle.call(part_list=part_list)
    return assembled

def test_and_maintenance(product_id):
    test_passed = TestSpindle.call(product_id=product_id)
    if not test_passed:
        print("Spindle sent to maintenance")
    return test_passed

def process(part_list, product_id):
    initiate_process_instance()
    if retrieve_and_setup(part_list):
        if assemble_spindle(part_list):
            test_result = test_and_maintenance(product_id)
            if test_result:
                print("Process completed successfully")
            else:
                print("Process completed with maintenance")
        else:
            print("Assembly failed")
    else:
        print("Failed to retrieve materials and set up")
    return "Process Ended"

if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  # Example part list
    product_id = 123  # Example product ID
    process_result = process(part_list, product_id)
    print(process_result)