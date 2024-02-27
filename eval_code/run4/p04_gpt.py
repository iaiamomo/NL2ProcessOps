from tools.manufacturer import SendSketches
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import OrderColor
from tools.printer_3d import HeatUpBedExtruder
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print
def instruct_artist_and_create_project():
    satisfied_with_result = False
    while not satisfied_with_result:
        # Assuming there's a tool or method to instruct the artist and provide feedback
        # which is not explicitly mentioned in the tools provided.
        # This placeholder represents the interaction with the artist.
        project_description = SendSketches.call()
        # Placeholder for providing feedback and checking satisfaction
        # This could involve more complex logic or user input in a real scenario
        satisfied_with_result = True  # Assuming satisfaction for simplicity
    return project_description

def manage_plastic_color():
    color = ChoosePlasticColor.call()
    quantity = CheckColorQuantity.call(color=color)
    if quantity < 100:
        # Assuming there's a method to add the color to the shopping list
        # This is a placeholder for that action
        print("Added color to shopping list")
    else:
        OrderColor.call(color=color)

def prepare_printer_and_print(project_description):
    HeatUpBedExtruder.call()
    gcode = GenerateGCode.call(project=project_description)
    Print.call(GCodeFile=gcode)

def process():
    project_description = instruct_artist_and_create_project()
    manage_plastic_color()
    prepare_printer_and_print(project_description)

if __name__ == "__main__":
    process()