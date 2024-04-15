import threading

class RecipeTest:
    description = {
        "name": "RecipeTest",
        "description": "Retrieve the recipe for testing.",
        "more details": "It takes as input the identificator of the product to be tested. It returns the recipe.",
        "input_parameters": ['product_id:int'],
        "output_parameters": ['recipe:list'],
        "actor": "cad_cam_is"
    }

    def call(product_id: int) -> list:
        recipe = ["test1", "test2"]
        return recipe
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return