
class L12SetUp:
    description = {
        "description": "Set up the L12 line",
        "more details": "This tool takes no input and returns a boolean indicating if the line has been set up.",
        "input_parameters": [],
        "output_parameters": ['set_up:bool'],
        "actor": "l12"
    }

    def call() -> bool:
        set_up = True
        return set_up


class L12Assemble:
    description = {
        "description": "Assembly of a product over the L12 line",
        "more details": "This tool takes as input the part list. It returns a boolean indicating if the product has been assembled.",
        "input_parameters": {
            'part_list': {'type': 'list', 'description': 'list of parts of a product'}
        },
        "output_parameters": {
            'assembled': {'type': 'bool', 'description': 'True if the product has been assembled, False otherwise'}
        },
        "actor": "l12"
    }

    def call(part_list: list) -> bool:
        assembled = True
        return assembled