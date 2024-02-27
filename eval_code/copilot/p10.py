from crm_is import ReceiveOrder, AcceptOrder
from manufacturer import InformStorehouseEngineering, AssembleBicycle
from wms_is import OrderRawMaterial

def process_order():
    # Sales department receives a new order
    part_list, product_id = ReceiveOrder.call()

    # Sales department can then reject or accept the order for a customized bike
    order_accepted = AcceptOrder.call(product_id)

    if not order_accepted:
        # If the order is rejected, the process instance is finished
        return "Order rejected."

    # If the order is accepted, the storehouse and the engineering department are informed
    InformStorehouseEngineering.call(part_list, product_id)

    # The storehouse immediately processes the part list of the order and checks the required quantity of each part
    for part in part_list:
        # If the part is not available, it is back-ordered
        OrderRawMaterial.call(part)

    # The engineering department prepares everything for the assembling of the ordered bicycle
    # If the storehouse has successfully reserved or back-ordered every item of the part list and the preparation activity has finished, the engineering department assembles the bicycle
    AssembleBicycle.call(part_list)

    # Afterwards, the sales department ships the bicycle to the customer and finishes the process instance
    return "Bicycle assembled and shipped to the customer."