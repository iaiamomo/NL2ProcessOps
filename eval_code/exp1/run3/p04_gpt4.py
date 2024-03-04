from tools.manufacturer import SendSketches
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import OrderColor
from tools.printer_3d import TurnOn
from tools.printer_3d import HeatUpBedExtruder
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print
def instruct_artist_and_print_model():
    # Instruct Artist and Send Sketches
    project_description = SendSketches.call()

    # Revise Project until satisfied
    satisfied = False
    while not satisfied:
        # Assuming a function to check if the manufacturer is satisfied
        # This could be replaced with actual logic to determine satisfaction
        satisfied = input("Are you satisfied with the project? (yes/no): ").lower() == "yes"
        if not satisfied:
            project_description = RefineRequirementsTreeHouse.call(part_list=[project_description])

    # Choose Plastic Color
    color = ChoosePlasticColor.call()

    # Check if Color is in Stock and its Quantity
    quantity = CheckColorQuantity.call(color=color)
    if quantity < 100:
        print("Adding color to shopping list as quantity is under 100g.")
        # Add to Shopping List (Assuming a function to add items to a shopping list)
        # This could be replaced with actual logic to add to a shopping list
    else:
        # Prepare Printer
        print("Preparing printer...")

    # Order Color if not in stock
    if quantity == 0:
        OrderColor.call(color=color)

    # Turn on the printer and heat up
    TurnOn.call()
    HeatUpBedExtruder.call()

    # Generate GCode
    gcode = GenerateGCode.call(project=project_description)

    # Print Model
    Print.call(GCodeFile=gcode)

    print("Model printing process completed.")

if __name__ == "__main__":
    instruct_artist_and_print_model()