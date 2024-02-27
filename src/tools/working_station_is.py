import random

class EmptyScan:
    description = {
        "description": "The working station system empty the scan result.",
        "more details": "It takes no input. It returns no output.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "working_station_is"
    }

    def call():
        return

class ScanOrder:
    description = {
        "description": "Worker scans the order.",
        "more details": "It takes no input. It returns the order id scanned.",
        "input_parameters": [],
        "output_parameters": ["order_id:int"],
        "actor": "working_station_is"
    }

    def call() -> int:
        # random order id
        order_id = random.randint(1, 100)
        return order_id


class DisplaysScanningUI:
    description = {
        "description": "The working station system displays the scanning UI.",
        "more details": "It takes no input. It returns no output.",
        "input_parameters": ["order_id:int"],
        "output_parameters": [],
        "actor": "working_station_is"
    }

    def call(order_id:int):
        return