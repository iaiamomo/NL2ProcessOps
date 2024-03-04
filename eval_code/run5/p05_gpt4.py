from tools.mold_is import SensorMeasure
from tools.mold_is import AnalyzeMold
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction
def monitor_injection_molding_process():
    # Measure the temperature, pressure, and fill rates of the mold
    temperature, pressure, fill_rate = SensorMeasure.call()
    
    # Analyze the measured parameters to check for deviations
    deviation = AnalyzeMold.call(temperature=temperature, pressure=pressure, fill_rate=fill_rate)
    
    # If there is a deviation, adjust the mold settings
    if deviation:
        AdjustMold.call()
        return "Adjustments made to the mold settings due to detected deviations."
    else:
        # If no deviations, authorize the production to continue
        AuthorizeProduction.call()
        return "Production authorized. Parameters are within the acceptable range."

if __name__ == "__main__":
    result = monitor_injection_molding_process()
    print(result)