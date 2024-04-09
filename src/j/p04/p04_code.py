from threading import Thread

# Assuming the tools are already imported as per the guidelines

def process():
    # Instruct Artist and Send Sketches (Assuming this is done outside the system as no tool is provided for these steps)
    project_description = SendSketches.call()
    
    # Choose Plastic Color
    color = ChoosePlasticColor.call()
    
    # Check Color Availability
    color_availability = CheckColorAvailability.call(color=color)
    
    if color_availability:
        # Check Color Quantity
        color_quantity = CheckColorQuantity.call(color=color)
        if color_quantity < 100:
            # Add to Shopping List (Assuming this is done outside the system as no tool is provided for this step)
            pass
    else:
        # Order Color
        OrderColor.call(color=color)
    
    # Prepare Printer (Assuming TurnOn and HeatUpBedExtruder are part of this step)
    TurnOn.call()
    
    # Parallel execution of Heating Up Printer and Generating GCode
    def heat_up_printer():
        HeatUpBedExtruder.call()
    
    def generate_gcode():
        gcode = GenerateGCode.call(project=project_description)
        return gcode
    
    thread1 = Thread(target=heat_up_printer)
    thread2 = Thread(target=generate_gcode)
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    gcode = thread2.join()  # Assuming we can capture the return value in this pseudo-code
    
    # Print Model
    Print.call(GCodeFile=gcode)

if __name__ == "__main__":
    process()