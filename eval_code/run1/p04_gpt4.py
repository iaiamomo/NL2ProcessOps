from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.printer_3d import TurnOn
from tools.printer_3d import HeatUpBedExtruder
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print
import threading

# Assuming the tools are already imported and available for use as described in the problem description.

def instruct_artist_and_get_project():
    project_description = SendSketches.call()
    satisfied = False
    while not satisfied:
        # Assuming there's a function to review the project and decide if satisfied or not.
        # This could be a user input or an automated check.
        satisfied = input("Are you satisfied with the project? (yes/no): ").lower() == "yes"
        if not satisfied:
            # Assuming a function to send revisions to the artist.
            # This could be a user input or an automated process.
            print("Sending revisions to the artist...")
            project_description = SendSketches.call()  # Simulating the revision process
    return project_description

def check_and_prepare_color():
    color = ChoosePlasticColor.call()
    quantity = CheckColorQuantity.call(color=color)
    if quantity < 100:
        print("Adding color to shopping list...")
        # Assuming a function to add items to a shopping list.
        # This could be a user input or an automated process.
    else:
        print("Color quantity is sufficient.")
    return color

def prepare_printer(project_description):
    TurnOn.call()
    HeatUpBedExtruder.call()
    gcode = GenerateGCode.call(project=project_description)
    return gcode

def print_model(gcode):
    Print.call(GCodeFile=gcode)

def process():
    project_description = instruct_artist_and_get_project()
    check_and_prepare_color()
    gcode = prepare_printer(project_description)
    print_model(gcode)
    print("Model printing process completed.")

if __name__ == "__main__":
    process()