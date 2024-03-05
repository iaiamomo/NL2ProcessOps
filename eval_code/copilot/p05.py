from mold_is import SensorMeasure, AnalyzeMold, AdjustMold, AuthorizeProduction

def quality_assurance_process():
    # Measure the temperature, pressure and fill rates of the mold
    temperature, pressure, fill_rate = SensorMeasure().call()

    # Analyze the measured data
    deviation = AnalyzeMold().call(temperature, pressure, fill_rate)

    # If any deviations are detected, adjust the settings
    if deviation:
        AdjustMold().call()

    # Once the parameters are within the acceptable range, authorize the production run to continue
    else:
        AuthorizeProduction().call()