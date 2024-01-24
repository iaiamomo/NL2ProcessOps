
class GetWordLength:
    description = {
        "description": """
        Useful for computing the length of a word.
        It takes as input a word.
        It returns the length of the word.
        """,
        "input_parameters": {
            'word': {'type': 'str', 'description': 'word to compute the length of'}
        },
        "output_parameters": {
            "length": {"type": "int", "description": "length of the word"}
        },
    }
    

    def call(word:str) -> int:
        length = len(word)
        return length