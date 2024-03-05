from manufacturer import SendSketches, ChoosePlasticColor, CheckColorAvailability, OrderColor, CheckColorQuantity, UpdateShoppingList, GenerateGCode
from printer_3d import TurnOn, HeatUpBedExtruder, Print

def create_custom_3d_model(sketches, changes, color, project):
    # Send sketches to the artist and tell him what to change
    SendSketches.call(sketches)
    for change in changes:
        # Assume that there is a function to send changes to the artist
        SendChangesToArtist.call(change)

    # Choose a plastic color for 3D printing
    ChoosePlasticColor.call(color)

    # Check if the color is available and if there is enough quantity
    if CheckColorAvailability.call(color):
        if CheckColorQuantity.call(color) < 100:
            UpdateShoppingList.call(color)
    else:
        OrderColor.call(color)

    # Turn the printer on and heat up the bed and the extruder
    TurnOn.call()
    HeatUpBedExtruder.call()

    # Generate the gcode file for the printer
    gcode = GenerateGCode.call(project)

    # Print the model
    Print.call(gcode)