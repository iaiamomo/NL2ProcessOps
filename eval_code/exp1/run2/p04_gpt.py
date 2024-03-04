from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import OrderColor
from tools.printer_3d import HeatUpBedExtruder
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
    if quantity == 0:
        OrderColor.call(color=color)
    return color

def print_model(project_description):
    HeatUpBedExtruder.call()
    gcode_file = GenerateGCode.call(project=project_description)
    Print.call(GCodeFile=gcode_file)

def process():
    project_description = instruct_artist_and_create_project()
    choose_and_prepare_color()
    print_model(project_description)
    return "Model printing process completed."

if __name__ == "__main__":
    result = process()
    print(result)