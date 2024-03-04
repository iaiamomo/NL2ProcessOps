from tools.mold_is import SensorMeasure
from tools.vision_is import CheckMarkers
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction
def check_parameters_against_standards(temperature, pressure, fill_rate):
    """
    This function simulates the analysis of the captured data against specified standards.
    It returns True if the parameters are within acceptable ranges, and False if adjustments are needed.
    """
    # Placeholder for actual logic to determine if parameters are within acceptable ranges.
    # For demonstration purposes, let's assume the standards are:
    # Temperature: 200-250, Pressure: 100-150, Fill Rate: 50-100
    if 200 <= temperature <= 250 and 100 <= pressure <= 150 and 50 <= fill_rate <= 100:
        return True
    else:
        return False

def process_injection_molding():
    while True:
        # Capture data from sensors
        temperature, pressure, fill_rate = SensorMeasure.call()
        
        # Analyze data to check if parameters are within acceptable ranges
        parameters_ok = check_parameters_against_standards(temperature, pressure, fill_rate)
        
        if not parameters_ok:
            # Adjust machine settings if deviations are detected
            AdjustMold.call()
        else:
            # Authorize production if parameters are acceptable
            AuthorizeProduction.call()
            break  # Exit the loop and end the process after authorizing production

if __name__ == "__main__":
    process_injection_molding()