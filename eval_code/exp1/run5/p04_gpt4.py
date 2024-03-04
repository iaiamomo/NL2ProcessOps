from tools.manufacturer import SendSketches
from tools.manufacturer import RefineRequirementsTreeHouse
from tools.manufacturer import ChoosePlasticColor
from tools.manufacturer import CheckColorQuantity
from tools.manufacturer import OrderColor
from tools.printer_3d import TurnOn
from tools.manufacturer import GenerateGCode
from tools.printer_3d import Print
def create_custom_3d_model():
    # Send sketches to the artist and get the project description
    project_description = SendSketches.call()

    # Assume there's a process of refining requirements that's iterative but not detailed here
    # This could involve multiple calls to RefineRequirementsTreeHouse with different part lists
    # For simplicity, we skip directly to choosing the plastic color

    # Choose the plastic color
    color = ChoosePlasticColor.call()

    # Check if the color is in stock and its quantity
    quantity = CheckColorQuantity.call(color=color)

    # If the quantity is under 100 grams or the color is not in stock, order the color
    if quantity < 100:
        OrderColor.call(color=color)

    # Turn on the 3D printer
    TurnOn.call()

    # Generate the GCode file for the printer from the project description
    gcode = GenerateGCode.call(project=project_description)

    # Print the model
    Print.call(GCodeFile=gcode)

    return "Model printing initiated."

if __name__ == "__main__":
    result = create_custom_3d_model()
    print(result)