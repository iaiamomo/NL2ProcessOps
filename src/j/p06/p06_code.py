from threading import Thread

# Assuming the tools are already imported as per the guidelines
# from tools import AcceptOrder, RetrieveRawMaterials, ConfigureAssemblyLine, CutMetal, AssembleParts, CheckQualityBrackets, EnhanceProduct

def process_order(product_id, part_list):
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return False

    def evaluate_parts_list():
        return RetrieveRawMaterials.call(part_list=part_list)

    def configure_robotic_assembly_line():
        ConfigureAssemblyLine.call()

    # Parallel execution of evaluating parts list and configuring assembly line
    parallel()
    thread1 = Thread(target=evaluate_parts_list)
    thread2 = Thread(target=configure_robotic_assembly_line)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end_parallel()

    CutMetal.call()
    AssembleParts.call()
    quality_ok = CheckQualityBrackets.call()

    if check(quality_ok):
        EnhanceProduct.call()
        return True
    else:
        return False

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['part1', 'part2', 'part3']  # Example part list
    process_result = process_order(product_id, part_list)
    print(f"Process completed successfully: {process_result}")