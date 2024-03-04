from tools.crm_is import ReceiveOrder
from tools.crm_is import AcceptOrder
from tools.manufacturer import InformStorehouseEngineering
from tools.manufacturer import SendRequirements
from tools.manufacturer import OrderParts
from tools.manufacturer import AssembleBicycle
def process_order():
    part_list, product_id = ReceiveOrder.call()
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return "Order Rejected"
    
    InformStorehouseEngineering.call(part_list=part_list, product_id=product_id)
    
    parts_reserved_or_backordered = True
    for part in part_list:
        # Assuming a hypothetical method to check and reserve or back-order parts
        # This is a simplification, as the actual implementation of checking availability,
        # reserving, or back-ordering parts would depend on the company's internal systems.
        part_available = check_and_reserve_or_backorder(part)
        if not part_available:
            parts_reserved_or_backordered = False
            break
    
    if parts_reserved_or_backordered:
        # Assuming preparation by the engineering department is done here
        # This is a simplification, as the actual implementation would likely involve
        # more detailed steps and checks.
        prepare_assembly(part_list)
        AssembleBicycle.call(part_list=part_list)
        # Assuming a method to ship the bicycle to the customer
        ship_bicycle(product_id)
        return "Order Processed and Bicycle Shipped"
    else:
        return "Order Failed due to Part Unavailability"

def check_and_reserve_or_backorder(part):
    # Placeholder for checking part availability and reserving or back-ordering
    # In a real scenario, this would involve inventory checks and possibly ordering parts
    return True  # Assuming all parts can be reserved or back-ordered for simplification

def prepare_assembly(part_list):
    # Placeholder for engineering department's preparation work
    pass

def ship_bicycle(product_id):
    # Placeholder for shipping the assembled bicycle to the customer
    pass

if __name__ == "__main__":
    result = process_order()
    print(result)