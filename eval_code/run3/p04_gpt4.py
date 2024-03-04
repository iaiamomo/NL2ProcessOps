from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import CheckColorAvailability
from tools.manufacturer import OrderColor
from tools.printer_3d import TurnOn
from tools.printer_3d import Print
from tools.printer_3d import HeatUpBedExtruder
from tools.manufacturer import GenerateGCode
def check_and_order_color(color):
    availability = CheckColorAvailability.call(color=color)
    if availability:
        quantity = CheckColorQuantity.call(color=color)
        if quantity < 100:
            print(f"Color {color} is under 100g, adding to shopping list.")
            # Add to shopping list (Assuming a function or a process for this exists)
        else:
            print(f"Color {color} is sufficient for printing.")
    else:
        print(f"Color {color} not in stock, ordering.")
        OrderColor.call(color=color)

def prepare_and_print(project):
    gcode = GenerateGCode.call(project=project)
    TurnOn.call()
    HeatUpBedExtruder.call()
    Print.call(GCodeFile=gcode)

def process():
    project_description = SendSketches.call()
    color = ChoosePlasticColor.call()
    check_and_order_color(color)
    prepare_and_print(project_description)
    print("Model printing process completed.")

if __name__ == "__main__":
    process()