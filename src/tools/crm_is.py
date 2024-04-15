import random
import threading

class ReceiveOrder:
    description = {
        "name": "ReceiveOrder",
        "description": "Sales department receives a new order specification from customer.",
        "more details": "It takes no input. It returns the part list and the product id.",
        "input_parameters": [],
        "output_parameters": ["part_list:list", "product_id:int"],
        "actor": "crm_is"
    }

    def call() -> list:
        n_elem = random.randint(1, 5)
        part_list = ["part" + str(i) for i in range(n_elem)]
        product_id = random.randint(1, 100)
        return part_list, product_id
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class AcceptOrder:
    description = {
        "name": "AcceptOrder",
        "description": "Sales department accepts the order.",
        "more details": "It takes the product id as input. It returns a boolean indicating if the order is accepted.",
        "input_parameters": ["product_id:int"],
        "output_parameters": ["order_accepted:bool"],
        "actor": "crm_is"
    }

    def call(product_id : int) -> bool:
        order_accepted = random.choice([True, False])
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class DeliverTestProtocol:
    description = {
        "name": "DeliverTestProtocol",
        "description": "Deliver the test protocol to the customer.",
        "more details": "It takes the protocol and the product id as input. It does not return anything.",
        "input_parameters": ["product_id:int", "protocol:str"],
        "output_parameters": [],
        "actor": "crm_is"
    }

    def call(product_id : int, protocol : str):
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return

class DeliverProduct:
    description = {
        "name": "DeliverProduct",
        "description": "Deliver the product to the customer.",
        "more details": "It takes the product id as input. It does not return anything.",
        "input_parameters": ["product_id:int"],
        "output_parameters": [],
        "actor": "crm_is"
    }

    def call(product_id : int):
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return