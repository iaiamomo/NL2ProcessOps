from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import CheckColorAvailability
from tools.manufacturer import OrderColor
from tools.printer_3d import HeatUpBedExtruder
from tools.printer_3d import TurnOn
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print
def instruct_artist():
    project_description = SendSketches.call()
    return project_description

def choose_plastic_color():
    color = ChoosePlasticColor.call()
    return color

def check_and_order_color(color):
    availability = CheckColorAvailability.call(color=color)
    if not availability:
        OrderColor.call(color=color)
    else:
        quantity = CheckColorQuantity.call(color=color)
        if quantity < 100:
            print("Adding color to shopping list.")
            # Add to shopping list (Assuming a function or a process for adding to shopping list exists)
        # If quantity is above 100g, no action needed as per process description

def prepare_printer():
    TurnOn.call()
    HeatUpBedExtruder.call()

def generate_gcode(project):
    gcode = GenerateGCode.call(project=project)
    return gcode

def print_model(gcode):
    Print.call(GCodeFile=gcode)

def process():
    project_description = instruct_artist()
    color = choose_plastic_color()
    check_and_order_color(color)
    prepare_printer()
    gcode = generate_gcode(project_description)
    print_model(gcode)
    return "Process completed."

if __name__ == "__main__":
    result = process()
    print(result)