from tools.mold_is import SensorMeasure
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction
def check_parameters(temperature, pressure, fill_rate):
    # Assuming there are predefined standards for temperature, pressure, and fill rate
    # These standards could be defined as global constants or retrieved from a database
    # For simplicity, we will define them as constants here
    STANDARD_TEMPERATURE = 200  # Example standard value
    STANDARD_PRESSURE = 1500  # Example standard value
    STANDARD_FILL_RATE = 300  # Example standard value

    # Check if the parameters are within acceptable ranges
    if (temperature == STANDARD_TEMPERATURE and
            pressure == STANDARD_PRESSURE and
            fill_rate == STANDARD_FILL_RATE):
        return True
    else:
        return False

def process():
    while True:
        # Capture data from sensors
        temperature, pressure, fill_rate = SensorMeasure.call()

        # Analyze data
        parameters_ok = check_parameters(temperature, pressure, fill_rate)

        if not parameters_ok:
            # Adjust machine settings if parameters are not acceptable
            AdjustMold.call()
        else:
            # Authorize production if parameters are acceptable
            AuthorizeProduction.call()
            break  # Exit the loop and end the process after authorizing production

if __name__ == "__main__":
    process()