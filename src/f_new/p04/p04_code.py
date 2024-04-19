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
    # Instruct the artist and send sketches
    project_description = SendSketches.call()

    # Assume a function to communicate changes until satisfied (not provided by tools)
    # This is a placeholder for the iterative process of revising the project
    # revise_project_until_satisfied(project_description)

    # Choose plastic color
    color = ChoosePlasticColor.call()

    # Check color availability
    color_availability = CheckColorAvailability.call(color=color)

    if color_availability:
        # Check color quantity
        quantity = CheckColorQuantity.call(color=color)
        if quantity < 100:
            # Add to shopping list if under 100g
            # Assume a function to add items to a shopping list (not provided by tools)
            # add_to_shopping_list(color)
            pass
    else:
        # Order color if not in stock
        OrderColor.call(color=color)

    # Prepare the printer
    TurnOn.call()
    HeatUpBedExtruder.call()

    # Generate GCode
    gcode = GenerateGCode.call(project=project_description)

    # Print the model
    Print.call(GCodeFile=gcode)

if __name__ == "__main__":
    instruct_artist_and_print_model()