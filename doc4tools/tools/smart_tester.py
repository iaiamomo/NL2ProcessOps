
class TestProduct:
    description = {
        "description": "Test and run-in of the product",
        "more details": "It takes as input the identificator of the product to be tested. It returns a boolean value, True if the product passed the test, False otherwise.",
        "input_parameters": ['product_id:int'],
        "output_parameters": ['passed:bool'],
        "actor": "smart_tester"
    }

    def call(product_id : int) -> bool:
        passed = True
        return passed
