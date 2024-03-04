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
def check_and_order_color(color):
    availability = CheckColorAvailability.call(color=color)
    if availability:
        quantity = CheckColorQuantity.call(color=color)
        if quantity < 100:
            print(f"Color {color} is under 100 grams, adding to shopping list.")
            # Here you would add the color to your shopping list. This is a placeholder.
            # In a real scenario, you might interact with a database or a shopping list app.
        else:
            print(f"Color {color} is sufficient for printing.")
    else:
        print(f"Color {color} is not available at home, ordering.")
        OrderColor.call(color=color)

def main_process():
    project_description = SendSketches.call()
    # Assuming there's a loop or interaction process for refining requirements not detailed here.
    # This would typically involve back-and-forth communication with the artist.
    # For simplicity, we're moving directly to choosing the plastic color.
    color = ChoosePlasticColor.call()
    check_and_order_color(color)
    TurnOn.call()
    HeatUpBedExtruder.call()
    gcode = GenerateGCode.call(project=project_description)
    Print.call(GCodeFile=gcode)
    print("Printing process started.")

if __name__ == "__main__":
    main_process()