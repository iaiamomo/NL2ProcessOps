from threading import Thread
def process():
    project_description = SendSketches.call()
    color = ChoosePlasticColor.call()
    color_availability = CheckColorAvailability.call(color=color)
    if check(color_availability):
        quantity = CheckColorQuantity.call(color=color)
        if check(quantity < 100):
            pass
    else:
        OrderColor.call(color=color)
    def prepare_printer():
        TurnOn.call()
        HeatUpBedExtruder.call()
    parallel()
    printer_preparation_thread = Thread(target=prepare_printer)
    printer_preparation_thread.start()
    gcode = GenerateGCode.call(project=project_description)
    printer_preparation_thread.join()  
    end_parallel()
    Print.call(GCodeFile=gcode)
if __name__ == "__main__":
    process()