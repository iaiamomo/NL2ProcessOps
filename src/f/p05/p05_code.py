def check_parameters(temperature, pressure, fill_rate):
    # Assuming there are predefined acceptable ranges for temperature, pressure, and fill rate
    # These ranges are placeholders and should be adjusted to the specific requirements of the process
    acceptable_temperature_range = (150, 300)  # Example range in degrees Celsius
    acceptable_pressure_range = (100, 200)  # Example range in bar
    acceptable_fill_rate_range = (50, 100)  # Example range in units per minute

    if (acceptable_temperature_range[0] <= temperature <= acceptable_temperature_range[1] and
        acceptable_pressure_range[0] <= pressure <= acceptable_pressure_range[1] and
        acceptable_fill_rate_range[0] <= fill_rate <= acceptable_fill_rate_range[1]):
        return True
    else:
        return False

def process():
    while True:
        # Capture data from sensors
        temperature, pressure, fill_rate = SensorMeasure.call()

        # Analyze data to check if parameters are within acceptable ranges
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