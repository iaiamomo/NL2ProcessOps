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
    # Assuming there's a tool or method to instruct the artist and provide feedback until satisfied
    # This is a placeholder for the loop logic to instruct the artist and provide feedback
    satisfied = False
    while not satisfied:
        project_description = SendSketches.call()
        # Placeholder for providing feedback and updating the satisfaction status
        # This could involve interaction with the artist, not detailed in the tools provided
        satisfied = True  # Assuming we're satisfied after the first iteration for simplicity
    return project_description

def choose_and_prepare_color():
    color = ChoosePlasticColor.call()
    availability = CheckColorAvailability.call(color=color)
    if availability:
        quantity = CheckColorQuantity.call(color=color)
        if quantity < 100:
            # Assuming there's a method to add the color to the shopping list
            print("Color added to shopping list")
    else:
        OrderColor.call(color=color)
    # Assuming the color is now ready for use
    return color

def print_model(project_description):
    TurnOn.call()
    HeatUpBedExtruder.call()
    gcode = GenerateGCode.call(project=project_description)
    Print.call(GCodeFile=gcode)

def main_process():
    project_description = instruct_artist_and_create_project()
    choose_and_prepare_color()
    print_model(project_description)

if __name__ == "__main__":
    main_process()