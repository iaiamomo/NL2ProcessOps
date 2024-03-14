from tree_sitter import Language, Parser
from utils import remove_comments_and_docstrings, tree_to_token_index, index_to_code_token
from DFG import DFG_python

PY_LANGUAGE = Language('../../build/my-languages.so', 'python')

def extract_dataflow(code, parsers):
    parser = parsers[0]
    dfg_parser = parsers[1]

    #remove comments
    try:
        code=remove_comments_and_docstrings(code)
    except:
        pass

    #obtain dataflow
    try:
        tree = parser.parse(bytes(code,'utf8'))
        root_node = tree.root_node

        tokens_index = tree_to_token_index(root_node)
        # elements of tokens_index are tuples of (start_point, end_point)
        # start_point and end_point are tuples of (row, column)

        code = code.split('\n')
        code_tokens = [index_to_code_token(x, code) for x in tokens_index]
        # code_tokens is a list of strings of the code tokens

        index_to_code={}
        for idx, (index, code) in enumerate(zip(tokens_index, code_tokens)):
            index_to_code[index] = (idx, code)
        # index_to_code is a dictionary with keys as tuples of (row, column) and values as tuples of (index, code)

        try:
            DFG, _ = dfg_parser(root_node, index_to_code, {}) 
        except Exception as e:
            print(e)
            DFG = []

        DFG = sorted(DFG, key = lambda x: x[1])
        indexs = set()
        for d in DFG:
            if len(d[-1]) != 0:
                indexs.add(d[1])
            for x in d[-1]:
                indexs.add(x)

        new_DFG=[]
        for d in DFG:
            if d[1] in indexs:
                new_DFG.append(d)
        dfg=new_DFG
    except Exception as e:
        print(e)
        dfg=[]
    return code_tokens, dfg

parser = Parser()
parser.set_language(PY_LANGUAGE)
#file_path = '../llm_process_code_spindle.py'
file_path = 'code.py'
with open(file_path, 'r') as file:
    code = file.read()

code_tokens, dfg = extract_dataflow(code, [parser, DFG_python])

tools = ["ReceiveOrder", "RetrievePartList", "L12SetUp", "L12AssembleSpindle", "TestSpindle"]
from concurrent.futures import ThreadPoolExecutor, as_completed
new_dfg = []
for elem in dfg:
    code, idx, txt_elem, from_elem, from_idx = elem
    if code == 'call':
        continue
    elif code in tools:
        continue
    new_dfg.append(elem)

new_dfg = sorted(new_dfg, key = lambda x: x[1])
for elem in new_dfg:
    print(elem)