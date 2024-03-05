from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
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
    quantity = CheckColorQuantity.call(color=color)
    if quantity < 100:
        print("Putting color on shopping list as quantity is under 100 grams.")
    else:
        print("Color is in stock and sufficient.")
    return color

def order_color_if_needed(color):
    if quantity < 100:
        OrderColor.call(color=color)
        print("Ordered more of the color as it was under 100 grams.")

def heat_up_printer_and_generate_gcode(project_description):
    HeatUpBedExtruder.call()
    gcode = GenerateGCode.call(project=project_description)
    return gcode

def print_model(gcode):
    TurnOn.call()
    Print.call(GCodeFile=gcode)

def main_process():
    project_description = instruct_artist_and_create_project()
    color = choose_and_prepare_color()
    order_color_if_needed(color)
    gcode = heat_up_printer_and_generate_gcode(project_description)
    print_model(gcode)
    print("Model printing process completed.")

if __name__ == "__main__":
    main_process()