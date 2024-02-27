from tools.mold_is import AuthorizeProduction
from tools.mold_is import SensorMeasure
from tools.mold_is import AnalyzeMold
from tools.mold_is import AdjustMold
def inject_mold_process():
    while True:
        # Inject molten plastic into mold (Assuming this is done implicitly as part of the cycle)
        
        # Capture data on temperature, pressure, and fill rates
        temperature, pressure, fill_rate = SensorMeasure.call()
        
        # Analyze data
        deviation = AnalyzeMold.call(temperature=temperature, pressure=pressure, fill_rate=fill_rate)
        
        if deviation:
            # Trigger adjustments to machine settings if deviations detected
            AdjustMold.call()
        else:
            # Continue production run if no deviations detected
            AuthorizeProduction.call()
            break  # Exit the loop and end the process after authorizing production

if __name__ == "__main__":
    inject_mold_process()