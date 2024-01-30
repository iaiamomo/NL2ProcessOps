
class ReceiveOrder:
    description = {
        "description": """
        The ERP receives an order.
        It takes no input.
        It returns the part list of the product.
        """,
        "input_parameters": { },
        "output_parameters": {
            "list_of_parts": {"type": "list", "description": "list of parts of the product"}
        },
        "actor": "erp_is"
    }

    def call() -> list:
        list_of_parts = ["part1", "part2", "part3"]
        return list_of_parts