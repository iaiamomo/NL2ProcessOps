from tools.manufacturer import SendSketches
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import CheckColorAvailability
from tools.manufacturer import OrderColor
from tools.printer_3d import HeatUpBedExtruder
from tools.printer_3d import TurnOn
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print
from threading import Thread

# Assuming all the tools are already imported as per the guidelines

def process():
    # Instruct the artist and send sketches
    project_description = SendSketches.call()
    
    # Revise the project until satisfied (not explicitly modeled, so we skip the implementation details)
    
    # Choose the plastic color
    color = ChoosePlasticColor.call()
    
    # Check color availability
    color_availability = CheckColorAvailability.call(color=color)
    
    if color_availability:
        # Check color quantity
        quantity = CheckColorQuantity.call(color=color)
        if quantity < 100:
            # Add to shopping list if under 100g
            # Assuming there's a function or method to add items to a shopping list
            add_to_shopping_list(color)
        # If enough stock or after adding to shopping list, proceed to turn on the printer
    else:
        # Order color if not in stock
        OrderColor.call(color=color)
    
    # Turn on the printer
    TurnOn.call()
    
    # Heat up the bed and the extruder in parallel with generating the GCode
    heat_up_thread = Thread(target=HeatUpBedExtruder.call)
    generate_gcode_thread = Thread(target=GenerateGCode.call, args=(project_description,))
    
    heat_up_thread.start()
    generate_gcode_thread.start()
    
    heat_up_thread.join()
    generate_gcode_thread.join()
    
    # Assuming GenerateGCode.call() returns a value that we capture
    gcode = GenerateGCode.call(project=project_description)
    
    # Print the model
    Print.call(GCodeFile=gcode)

def add_to_shopping_list(item):
    # Placeholder function to simulate adding items to a shopping list
    print(f"Adding {item} to the shopping list.")

if __name__ == "__main__":
    process()