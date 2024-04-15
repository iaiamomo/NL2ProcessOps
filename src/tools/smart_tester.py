import threading

class TestSpindle:
    description = {
        "name": "TestSpindle",
        "description": "Test and run-in of the spindle.",
        "more details": "It takes as input the identificator of the product to be tested. It returns a boolean value, True if the spindle passed the test, False otherwise.",
        "input_parameters": ['product_id:int'],
        "output_parameters": ['passed:bool'],
        "actor": "smart_tester"
    }

    def call(product_id : int) -> bool:
        passed = True
        return passed
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return
