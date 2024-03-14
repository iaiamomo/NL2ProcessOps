from io import StringIO
import tokenize # for tokenizing the code (python)
import ast
from graphviz import Digraph


def remove_comments_and_docstrings(source):
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
        # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    temp=[]
    for x in out.split('\n'):
        if x.strip()!="":
            temp.append(x)
    return '\n'.join(temp)


def annotate(source):
    modified_code = []
    in_parallel_block = False
    for line in source:
        if 'threading.Thread' in line and not in_parallel_block:
            num_spaces = 0
            for char in line:
                if char == ' ':
                    num_spaces += 1
                else:
                    break
            modified_code.append(' ' * num_spaces + 'parallel()')
            modified_code.append(line)
            in_parallel_block = True
            continue
        if 'join()' in line and in_parallel_block:
            num_spaces = 0
            for char in line:
                if char == ' ':
                    num_spaces += 1
                else:
                    break
            modified_code.append(line)
            modified_code.append(' ' * num_spaces + 'end_parallel()')
            in_parallel_block = False
            continue
        if 'if' in line or 'elif' in line:
            # extract the condition
            condition = line.split('if')[-1].strip().split(':')[0]
            modified_code.append(f'if condition({condition})')
            continue
        modified_code.append(line)
    return modified_code


def extract_ast(code):
    tree = ast.parse(code)
    print(ast.dump(tree))
    input()

    # Create a Graphviz Digraph object
    dot = Digraph()

    # Define a function to recursively add nodes to the Digraph
    def add_node(node, parent=None):
        node_name = str(node.__class__.__name__)
        dot.node(str(id(node)), node_name)
        if parent:
            dot.edge(str(id(parent)), str(id(node)))
        for child in ast.iter_child_nodes(node):
            add_node(child, node)

    # Add nodes to the Digraph
    add_node(tree)

    # Render the Digraph as a PNG file
    dot.format = 'png'
    dot.render('my_ast', view=True)

if __name__ == "__main__":
    file_path = 'p01_gpt4.py'
    with open(file_path, 'r') as file:
        code = file.read()
    code = remove_comments_and_docstrings(code)
    print(code)
    extract_ast(code)



    #code_lines = code.split('\n')
    #modified_code = annotate(code_lines)
    #print('\n'.join(modified_code))