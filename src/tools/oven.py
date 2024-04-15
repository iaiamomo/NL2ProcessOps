import threading

class Cook:
    description = {
        "name": "Cook",
        "description": "Cook a product in the oven.",
        "more details": "It takes as input the id of the product to be cooked. It returns a boolean value, True if the product has been cooked, False otherwise.",
        "input_parameters": ["product_id:int"],
        "output_parameters": ['cooked:bool'],
        "actor": "machine"
    }

    def call(product_id : int) -> bool:
        cooked = True
        return cooked
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return
