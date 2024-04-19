from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import CheckColorAvailability
from tools.manufacturer import OrderColor
from tools.printer_3d import HeatUpBedExtruder
from tools.printer_3d import TurnOn
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print

def instruct_artist_and_print_model():
    project_description = SendSketches.call()
    color = ChoosePlasticColor.call()
    color_availability = CheckColorAvailability.call(color=color)
    if beautiful_pipeline_check(color_availability):
        quantity = CheckColorQuantity.call(color=color)
        if beautiful_pipeline_check(quantity < 100):
            pass
    else:
        OrderColor.call(color=color)
    TurnOn.call()
    HeatUpBedExtruder.call()
    gcode = GenerateGCode.call(project=project_description)
    Print.call(GCodeFile=gcode)
if __name__ == "__main__":
    instruct_artist_and_print_model()