
class ProductMaintenance:
    description = {
        "description": """
        Useful for maintaining a product.
        It takes as input the identificator of the product to be maintained and does not return anything.
        """,
        "input_parameters": {
            'product_id': {'type': 'int', 'description': 'identificator of the product'}
        },
        "output_parameters": {},
        "actor": "cmms_is"
    }

    def call(product_id: int):
        pass