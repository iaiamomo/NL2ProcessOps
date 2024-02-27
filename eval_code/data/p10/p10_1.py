from tools.crm_is import ReceiveOrder, AcceptOrder, DeliverProduct
from tools.wms_is import RetrieveRawMaterial, OrderRawMaterial
from tools.assembly_line import ConfigureAssemblyLine
from tools.manufacturer import AssembleBicycle, InformStorehouseEngineering

from threading import Thread

def ordermaterials(part_list):
    for part in part_list:
        retrieved = RetrieveRawMaterial.call(part)

        if not retrieved:
            OrderRawMaterial.call(part)

def assemblyline():
    ConfigureAssemblyLine.call()

def process():
    part_list, product_id = ReceiveOrder.call()

    accepted = AcceptOrder.call(product_id)

    if not accepted:
        return
    
    InformStorehouseEngineering.call(part_list, product_id)
    
    t1 = Thread(target=ordermaterials, args=(part_list,))
    t2 = Thread(target=assemblyline)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    AssembleBicycle.call(part_list)

    DeliverProduct.call(product_id)

if __name__ == '__main__':
    process()