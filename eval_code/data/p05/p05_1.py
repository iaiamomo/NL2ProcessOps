from tools.mold_is import SensorMeasure, AnalyzeMold, AdjustMold, AuthorizeProduction

def process():
    temperature, pressure, fill_rate = SensorMeasure.call()

    deviation = AnalyzeMold.call(temperature, pressure, fill_rate)

    if deviation:
        AdjustMold.call()
    
    AuthorizeProduction.call()

if __name__ == "__main__":
    process()