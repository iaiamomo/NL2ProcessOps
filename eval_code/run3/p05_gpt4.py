from tools.mold_is import SensorMeasure
from tools.mold_is import AnalyzeMold
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction
def quality_assurance_process():
    while True:
        # Capture data from sensors
        temperature, pressure, fill_rate = SensorMeasure.call()
        
        # Analyze captured data for deviations
        deviation = AnalyzeMold.call(temperature=temperature, pressure=pressure, fill_rate=fill_rate)
        
        if deviation:
            # Adjust machine settings if deviations are detected
            AdjustMold.call()
        else:
            # Authorize production if parameters are acceptable
            AuthorizeProduction.call()
            break  # Exit the loop once production is authorized

if __name__ == "__main__":
    quality_assurance_process()