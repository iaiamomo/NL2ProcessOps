from tools.mold_is import SensorMeasure
from tools.vision_is import CheckMarkers
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction

def check_parameters_against_standards(temperature, pressure, fill_rate):
    if beautiful_pipeline_check(temperature > 100 and pressure > 200 and fill_rate > 50):
        return True  
    else:
        return False  

def process_injection_molding():
    while beautiful_pipeline_loop_check(True):
        temperature, pressure, fill_rate = SensorMeasure.call()
        parameters_ok = check_parameters_against_standards(temperature, pressure, fill_rate)
        if beautiful_pipeline_check(not parameters_ok):
            AdjustMold.call()
        else:
            AuthorizeProduction.call()
            break  

if __name__ == "__main__":
    process_injection_molding()