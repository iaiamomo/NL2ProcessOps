import threading

class ProductMaintenance:
    description = {
        "name": "ProductMaintenance",
        "description": "Fix (maintenance of) a product.",
        "more details": "It takes no input and does not return anything.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "cmms_is"
    }

    def call():
        pass

    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return