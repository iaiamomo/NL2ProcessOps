
class ReceiveOrder:
    description = {
        "description": """
        Useful for receiving an order.
        This tool takes as input the id of the product to be produced.
        It returns the part list of the product.
        """,
        "input_parameters": {
            'product_id': {'type': 'int', 'description': 'product identifier to be produced'}
        },
        "output_parameters": {
            "list_of_parts": {"type": "list", "description": "list of parts of the product"}
        },
        "actor": "erp_is"
    }

    def call(product_id: str) -> list:
        list_of_parts = ["part1", "part2", "part3"]
        return list_of_parts