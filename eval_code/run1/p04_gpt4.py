from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorAvailability
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import OrderColor
from tools.printer_3d import HeatUpBedExtruder
from tools.printer_3d import TurnOn
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print
def instruct_artist_and_print_model():
    # Instruct the artist by sending sketches and revising until satisfied
    project_description = SendSketches.call()
    satisfied = False
    while not satisfied:
        # Assume a function revise_sketches() exists that returns True if satisfied, False otherwise
        satisfied = revise_sketches(project_description)
    
    # Choose plastic color
    color = ChoosePlasticColor.call()
    
    # Check color availability and quantity
    color_availability = CheckColorAvailability.call(color=color)
    if color_availability:
        color_quantity = CheckColorQuantity.call(color=color)
        if color_quantity < 100:
            add_to_shopping_list(color)
    else:
        OrderColor.call(color=color)
    
    # Prepare the printer
    prepare_printer()
    
    # Generate GCode
    gcode = GenerateGCode.call(project=project_description)
    
    # Print the model
    Print.call(GCodeFile=gcode)

def revise_sketches(project_description):
    # This is a placeholder for the logic to decide if the sketches need more revisions
    # For the purpose of this example, let's assume we're always satisfied after the first revision
    return True

def add_to_shopping_list(color):
    # Placeholder for adding the color to a shopping list
    print(f"Added color {color} to the shopping list.")

def prepare_printer():
    # Turn on the printer and heat up the bed and the extruder
    TurnOn.call()
    HeatUpBedExtruder.call()

if __name__ == "__main__":
    instruct_artist_and_print_model()