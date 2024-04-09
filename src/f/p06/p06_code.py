import threading

def process_order(product_id, part_list):
    # Accept the order
    order_accepted = AcceptOrder.call(product_id=product_id)
    if not order_accepted:
        return False

    # Parallel execution for evaluating parts list and configuring the robotic assembly line
    def evaluate_parts():
        nonlocal parts_retrieved
        parts_retrieved = RetrieveRawMaterials.call(part_list=part_list)

    def configure_assembly_line():
        ConfigureAssemblyLine.call()

    parts_retrieved = False
    thread1 = threading.Thread(target=evaluate_parts)
    thread2 = threading.Thread(target=configure_assembly_line)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    if not parts_retrieved:
        return False

    # Sequential tasks for cutting metal, assembling brackets, and inspecting brackets
    CutMetal.call()
    AssembleParts.call()
    quality_ok = CheckQualityBrackets.call()

    if not quality_ok:
        return False

    # Apply coating if brackets are of good quality
    EnhanceProduct.call()

    return True

if __name__ == "__main__":
    product_id = 123  # Example product ID
    part_list = ['part1', 'part2', 'part3']  # Example part list
    process_result = process_order(product_id, part_list)
    if process_result:
        print("Process completed successfully.")
    else:
        print("Process terminated due to an error or rejection.")