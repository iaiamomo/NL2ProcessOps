from tools.mold_is import SensorMeasure
from tools.mold_is import AnalyzeMold
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction
def plastic_injection_molding_process():
    while True:
        # Capture data from sensors
        temperature, pressure, fill_rate = SensorMeasure.call()
        
        # Analyze captured data for deviations
        deviation_detected = AnalyzeMold.call(temperature=temperature, pressure=pressure, fill_rate=fill_rate)
        
        if deviation_detected:
            # Adjust machine settings if deviations are detected
            AdjustMold.call()
        else:
            # Authorize production if parameters are acceptable
            AuthorizeProduction.call()
            break  # Exit the loop once production is authorized

if __name__ == "__main__":
    plastic_injection_molding_process()