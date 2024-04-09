def check_parameters(temperature, pressure, fill_rate):
    acceptable_temperature_range = (150, 300)  
    acceptable_pressure_range = (100, 200)  
    acceptable_fill_rate_range = (50, 100)  
    if check((acceptable_temperature_range[0] <= temperature <= acceptable_temperature_range[1] and
        acceptable_pressure_range[0] <= pressure <= acceptable_pressure_range[1] and
        acceptable_fill_rate_range[0] <= fill_rate <= acceptable_fill_rate_range[1])):
        return True
    else:
        return False
def process():
    while True:
        temperature, pressure, fill_rate = SensorMeasure.call()
        parameters_ok = check_parameters(temperature, pressure, fill_rate)
        if check(not parameters_ok):
            AdjustMold.call()
        else:
            AuthorizeProduction.call()
            break  
if __name__ == "__main__":
    process()