
class L12SetUp:
    description = {
        "description": """
        Useful for setting up the L12 line.
        This tool takes no input and returns a boolean indicating if the line has been set up.
        """,
        "input_parameters": {},
        "output_parameters": {
            'set_up': {'type': 'bool', 'description': 'True if the line has been set up, False otherwise'}
        },
        "actor": "l12"
    }

    def call() -> bool:
        set_up = True
        return set_up


class L12AssembleSpindle:
    description = {
        "description": """
        Useful for assembling a spindle.
        This tool takes as input the part list of a spindle.
        It returns a boolean indicating if the spindle has been assembled.
        """,
        "input_parameters": {
            'part_list': {'type': 'list', 'description': 'list of parts of a spindle'}
        },
        "output_parameters": {
            'assembled': {'type': 'bool', 'description': 'True if the spindle has been assembled, False otherwise'}
        },
        "actor": "l12"
    }

    def call(part_list: list) -> bool:
        assembled = True
        return assembled