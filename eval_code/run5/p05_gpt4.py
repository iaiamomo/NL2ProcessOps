from tools.mold_is import SensorMeasure
from tools.mold_is import AnalyzeMold
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction
def quality_assurance_process():
    # Measure the temperature, pressure, and fill rates of the mold
    temperature, pressure, fill_rate = SensorMeasure.call()
    
    # Analyze the measured parameters to check for deviations
    deviation = AnalyzeMold.call(temperature=temperature, pressure=pressure, fill_rate=fill_rate)
    
    # If there is a deviation, adjust the mold settings
    if deviation:
        AdjustMold.call()
        return "Adjustments made. Re-check parameters."
    else:
        # If there are no deviations, authorize the production
        AuthorizeProduction.call()
        return "Production authorized."

if __name__ == "__main__":
    result = quality_assurance_process()
    print(result)