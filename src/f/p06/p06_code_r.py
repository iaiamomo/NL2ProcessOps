import threading
def process_order(product_id, part_list):
    order_accepted = AcceptOrder.call(product_id=product_id)
    if check(not order_accepted):
        return False
    def evaluate_parts():
        nonlocal parts_retrieved
        parts_retrieved = RetrieveRawMaterials.call(part_list=part_list)
    def configure_assembly_line():
        ConfigureAssemblyLine.call()
    parts_retrieved = False
    parallel()
    thread1 = threading.Thread(target=evaluate_parts)
    thread2 = threading.Thread(target=configure_assembly_line)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end_parallel()
    if check(not parts_retrieved):
        return False
    CutMetal.call()
    AssembleParts.call()
    quality_ok = CheckQualityBrackets.call()
    if check(not quality_ok):
        return False
    EnhanceProduct.call()
    return True
if __name__ == "__main__":
    product_id = 123  
    part_list = ['part1', 'part2', 'part3']  
    process_result = process_order(product_id, part_list)
    if check(process_result):
        print("Process completed successfully.")
    else:
        print("Process terminated due to an error or rejection.")