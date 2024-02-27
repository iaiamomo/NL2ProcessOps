import random

class SensorMeasure:
    description = {
        "description": "Measure the temperature, pressure and fill rates of the mold.",
        "more details": "It takes no input and returns the temperature of the oven.",
        "input_parameters": [],
        "output_parameters": ['temperature:int', 'pressure:int', 'fill_rate:int'],
        "actor": "mold_is"
    }

    def call() -> int:
        temperature = random.randint(0, 100)
        pressure = random.randint(0, 100)
        fill_rate = random.randint(0, 100)
        return temperature, pressure, fill_rate

class AnalyzeMold:
    description = {
        "description": "Analyze the temperature, pressure and fill rates of the mold to check deviations.",
        "more details": "It takes the temperature, pressure and fill rate as input and returns a boolean indicating if the mold is ok.",
        "input_parameters": ['temperature:int', 'pressure:int', 'fill_rate:int'],
        "output_parameters": ['deviation:bool'],
        "actor": "mold_is"
    }

    def call(temperature: int, pressure: int, fill_rate: int) -> bool:
        deviation = random.choice([True, False])
        return deviation

class AdjustMold:
    description = {
        "description": "Adjust the settings the mold.",
        "more details": "It takes no input and returns no output.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "mold_is"
    }

    def call():
        return

class AuthorizeProduction:
    description = {
        "description": "Authorize the production of the mold.",
        "more details": "It takes no input and returns no output.",
        "input_parameters": [],
        "output_parameters": [],
        "actor": "mold_is"
    }

    def call():
        return