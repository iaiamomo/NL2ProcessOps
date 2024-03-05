from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import CheckColorAvailability
from tools.manufacturer import OrderColor
from tools.printer_3d import HeatUpBedExtruder
from tools.printer_3d import TurnOn
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print
def instruct_artist_and_create_project():
    satisfied = False
    while not satisfied:
        project_description = SendSketches.call()
        feedback = input("Provide feedback to the artist (type 'satisfied' to proceed): ")
        if feedback.lower() == 'satisfied':
            satisfied = True
    return project_description

def choose_and_prepare_color():
    color = ChoosePlasticColor.call()
    availability = CheckColorAvailability.call(color=color)
    if availability:
        quantity = CheckColorQuantity.call(color=color)
        if quantity < 100:
            print("Color quantity under 100 grams. Adding to shopping list.")
    else:
        OrderColor.call(color=color)
    return color

def prepare_printer_and_print(project_description):
    TurnOn.call()
    HeatUpBedExtruder.call()
    gcode = GenerateGCode.call(project=project_description)
    Print.call(GCodeFile=gcode)

def process():
    project_description = instruct_artist_and_create_project()
    color = choose_and_prepare_color()
    prepare_printer_and_print(project_description)

if __name__ == "__main__":
    process()