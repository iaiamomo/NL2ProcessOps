import threading
def initiate_process_instance():
    print("New process instance initiated")
def retrieve_and_setup(part_list):
    def retrieve():
        retrieved = RetrieveRawMaterials.call(part_list=part_list)
        return retrieved
    def setup():
        set_up = L12SetUp.call()
        return set_up
    parallel()
    retrieve_thread = threading.Thread(target=retrieve)
    setup_thread = threading.Thread(target=setup)
    retrieve_thread.start()
    setup_thread.start()
    retrieve_thread.join()
    setup_thread.join()
    end_parallel()
    return True
def assemble_spindle(part_list):
    assembled = L12AssembleSpindle.call(part_list=part_list)
    return assembled
def test_and_maintenance(product_id):
    test_passed = TestSpindle.call(product_id=product_id)
    if check(not test_passed):
        print("Spindle sent to maintenance")
    return test_passed
def process(part_list, product_id):
    initiate_process_instance()
    if check(retrieve_and_setup(part_list)):
        if check(assemble_spindle(part_list)):
            test_result = test_and_maintenance(product_id)
            if check(test_result):
                print("Process completed successfully")
            else:
                print("Process completed with maintenance")
        else:
            print("Assembly failed")
    else:
        print("Failed to retrieve materials and set up")
    return "Process Ended"
if __name__ == "__main__":
    part_list = ["part1", "part2", "part3"]  
    product_id = 123  
    process_result = process(part_list, product_id)
    print(process_result)