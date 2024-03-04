from tools.mold_is import AuthorizeProduction
from tools.mold_is import SensorMeasure
class AuthorizeProduction:
    @staticmethod
    def call():
        # This method simulates authorizing the production run
        print("Production authorized.")

class SensorMeasure:
    @staticmethod
    def call():
        # This method simulates measuring the temperature, pressure, and fill rates
        # For the sake of example, let's return some dummy values
        return 100, 200, 300  # temperature, pressure, fill_rate

def analyze_data(temperature, pressure, fill_rate):
    # This function simulates analyzing the captured data
    # Let's assume the specified standards are:
    # Temperature: 100 +/- 10, Pressure: 200 +/- 20, Fill Rate: 300 +/- 30
    if (90 <= temperature <= 110) and (180 <= pressure <= 220) and (270 <= fill_rate <= 330):
        return True  # No deviations detected
    else:
        return False  # Deviations detected

def trigger_adjustments():
    # This function simulates triggering adjustments to the machine settings
    print("Adjustments to machine settings have been triggered.")

def inject_molten_plastic_into_mold():
    # This function simulates the injection of molten plastic into the mold
    print("Molten plastic injected into mold.")

def continue_production_run():
    # This function simulates continuing the production run
    AuthorizeProduction.call()

def quality_assurance_process():
    inject_molten_plastic_into_mold()
    while True:
        temperature, pressure, fill_rate = SensorMeasure.call()
        if analyze_data(temperature, pressure, fill_rate):
            continue_production_run()
            break
        else:
            trigger_adjustments()

if __name__ == "__main__":
    quality_assurance_process()