from tools.manufacturer import SendSketches, ChoosePlasticColor, CheckColorAvailability, CheckColorQuantity, OrderColor, UpdateShoppingList, GenerateGCode
from tools.printer_3d import TurnOn, Print, HeatUpBedExtruder

from threading import Thread
from queue import Queue

def turnon():
    TurnOn.call()

def generategcode(project, results_queue):
    gcode = GenerateGCode.call(project)
    results_queue.put(gcode)

def heatup():
    HeatUpBedExtruder.call()

def process():
    project = SendSketches.call()

    color = ChoosePlasticColor.call()

    available = CheckColorAvailability.call(color)

    if not available:
        OrderColor.call(color)
    else:
        quantity = CheckColorQuantity.call(color)
        if quantity < 100:
            UpdateShoppingList.call(color)

    results_queue = Queue()
    thread_turnon = Thread(target=turnon)
    thread_generategcode = Thread(target=generategcode, args=(project, results_queue))
    thread_heatup = Thread(target=heatup)
    thread_turnon.start()
    thread_generategcode.start()
    thread_heatup.start()
    thread_turnon.join()
    thread_generategcode.join()
    thread_heatup.join()

    gcode = results_queue.get()

    Print.call(gcode)

if __name__ == "__main__":
    process()