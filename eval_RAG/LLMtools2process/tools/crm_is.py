
class ReceiveOrder:
    description = {
        "description": "Sales department receives a new order.",
        "more details": "It takes no input. It returns the part list and the product id.",
        "input_parameters": [],
        "output_parameters": ["list_of_parts:list", "product_id:int"],
        "actor": "crm_is"
    }

    def call() -> list:
        list_of_parts = ["part1", "part2", "part3"]
        product_id = 1
        return list_of_parts, product_id