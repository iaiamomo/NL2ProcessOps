from tools.crm_is import ReceiveOrder
from tools.manufacturer import AssembleBicycle
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.crm_is import DeliverProduct
import threading

def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = True  # Assuming the order is accepted for the sake of this example

    if not order_accepted:
        return "Order Rejected"

    def process_part_list(part_list):
        for part in part_list:
            part_available = True  # Assuming part availability check logic
            if part_available:
                ReservePart.call(part=part)
            else:
                BackOrderPart.call(part=part)

    def prepare_for_assembling(part_list, product_id):
        InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)

    # Parallel execution of storehouse processing and engineering preparation
    threads = []
    thread1 = threading.Thread(target=process_part_list, args=(part_list,))
    thread2 = threading.Thread(target=prepare_for_assembling, args=(part_list, product_id))
    threads.append(thread1)
    threads.append(thread2)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    AssembleBicycle.call(part_list=part_list)
    DeliverProduct.call(product_id=product_id)

    return "Order Processed and Bicycle Delivered"

if __name__ == "__main__":
    result = process_order()
    print(result)