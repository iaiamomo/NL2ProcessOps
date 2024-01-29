
class RecipeTest:
    description = {
        "description": """
        Useful for retrieving the recipe for testing a product.
        It takes as input the identificator of the product.
        It returns the recipe of the product to be tested.
        """,
        "input_parameters": {
            'product_id': {'type': 'int', 'description': 'identificator of the product'}
        },
        "output_parameters": {
            'recipe': {'type': 'list', 'description': 'recipe of the product to be tested'}
        },
        "actor": "recipe_test"
    }

    def call(product_id: int) -> list:
        recipe = ["test1", "test2"]
        return recipe