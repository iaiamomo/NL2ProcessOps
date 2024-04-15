import threading

class PalletArrives:
    description = {
        "name": "PalletArrives",
        "description": "Pallet arrives at the working station.",
        "more details": "It takes no input. It returns no output.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "pallet"
    }

    def call():
        return
    
    def fake_call():
        # print the class description and the thread id where the tool is called
        print(f"{__class__.description} - {threading.get_ident()}")
        return