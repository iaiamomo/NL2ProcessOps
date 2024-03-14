import tree_sitter
from tree_sitter import Language, Parser

# Load the Python language library
PY_LANGUAGE = Language('../build/my-languages.so', 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

def extract_data_flow(file_path):
    # Read the file
    with open(file_path, 'r') as file:
        code = file.read()

    # Parse the code
    tree = parser.parse(bytes(code, 'utf8'))

    # Extract the variable sequence and relationships
    var_sequence = []
    var_relationships = {}

    def traverse(node):
        if node.type == 'identifier':
            var_sequence.append(node)
        elif node.type == 'assignment':
            var = node.children[0].children[0]
            value = node.children[2]
            if var.type == 'identifier' and value.type == 'identifier':
                if var not in var_relationships:
                    var_relationships[var] = []
                var_relationships[var].append(value)
        for child in node.children:
            traverse(child)

    traverse(tree.root_node)

    # Convert the variable sequence and relationships to a more readable format
    var_sequence = [node.text(code).decode('utf8') for node in var_sequence]
    var_relationships = {node.text(code).decode('utf8'): [value.text(code).decode('utf8') for value in values] for node, values in var_relationships.items()}

    return var_sequence, var_relationships

# Test the function
print(extract_data_flow('llm_process_code_spindle.py'))