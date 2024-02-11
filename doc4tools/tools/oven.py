
class Cook:
    description = {
        "description": "Cook a product in the oven",
        "more details": "It takes as input the id of the product to be cooked. It returns a boolean value, True if the product has been cooked, False otherwise.",
        "input_parameters": ["product_id:int"],
        "output_parameters": ['cooked:bool'],
        "actor": "oven"
    }

    def call(product_id : int) -> bool:
        cooked = True
        return cooked
