from pathlib import Path
import os
import sys
import json
for i in range(5):
    if not (Path.cwd()/"rule_status_assessment").exists(): os.chdir(Path.cwd().parent.as_posix())
    else: sys.path.append(Path.cwd().as_posix())

from pathlib import Path

####################################################
# Formula Parsing script
####################################################
# Noel Brindise, Sept 2024
#
# Purpose: process LTL formulas expressed as strings into an LTL tree format
# Input: str 
# Output: formula tree as a list of lists
#
# Howto: 
# 
#   Call parse_formula() for a string
#   ex1) parse_formula('dog U (cat and frog)')
#   ex2) parse_formula('a AND b implies c X d')
#
#   Input format: parser recognizes...
#       -parentheses as grouping symbols
#       -LTL operators 'G', 'X', 'F', 'U', 'W', 'M', 'R' (case sensitive!)
#       -Not: 'not', 'neg' (not case sensitive)
#       -Implication: '->', 'implies' (not c.s.)
#       -Or: 'or' (not c.s.)
#       -And: 'and' (not c.s.)
#
#   Other lowercase/numerical strings will be recognized as 'labels'*, e.g.
#       - 'dog or (fish U dry)' will identify 'dog', 'fish', 'dry' as labels
#
#       * Labels must be separated either by spaces, grouping symbols, or the string '->'
#         Key words within labels will not be recognized as key words other than:
#           '->', '(', ')', 'X', 'F', 'G'... (case sensitive)
#           e.g. 'hand' will be parsed as a label 'hand', not label 'h' + operator 'AND'
#                'abUfe' will be parsed as 'ab' U 'fe'

####################################################
# 
####################################################

def index_formula(raw_str):
    # Identifies operators and atoms and indexes them.
    op_idxs = list()
    paren_map = list()
    operator_strength = list()
    empty_tree_nodes = list()
    label_list = list()
    
    # Add extra terminal spaces for processing purposes:
    formula_str = ''.join([' ',raw_str, '  '])

    # Initialize parenthetical grouping level to 0:
    paren_level = 0
    
    # Initialize empty atom string
    atom = ''
    
    i = 1

    while i < len(raw_str) + 1:

        #'or' surrounded by ')', '(', and/or spaces:
        if formula_str[i:i+2] in ['or','OR','Or'] and formula_str[i-1] in [')',' '] and formula_str[i+2] in ['(',' ']:
            op_idxs.append('or')
            paren_map.append(paren_level)
            operator_strength.append(0)
            empty_tree_nodes.append(["or",list(),list()])
            i = i+2
        #'and' surrounded by ')', '(', and/or spaces:
        elif formula_str[i:i+3] in ['and', 'AND','And'] and formula_str[i-1] in [')',' '] and formula_str[i+3] in ['(',' ']:
            op_idxs.append('and')
            paren_map.append(paren_level)
            operator_strength.append(0)
            empty_tree_nodes.append(["and",list(),list()])
            i = i+3
            
        # '->':
        elif formula_str[i:i+2] == '->':
            op_idxs.append('->')
            paren_map.append(paren_level)
            operator_strength.append(0)
            empty_tree_nodes.append(["->",list(),list()])
            i = i+2
        # 'implies':
        elif formula_str[i:i+7] in ['implies','IMPLIES','Implies']:
            op_idxs.append('->')
            paren_map.append(paren_level)
            operator_strength.append(0)
            empty_tree_nodes.append(["->",list(),list()])
            i = i+7
            
        # Binary operators:
        elif formula_str[i] == 'U':
            op_idxs.append('U')  
            paren_map.append(paren_level)
            operator_strength.append(1)
            empty_tree_nodes.append(["U",list(),list()])
            i = i+1
        elif formula_str[i] == 'R':
            op_idxs.append('R') 
            paren_map.append(paren_level)
            operator_strength.append(1)
            empty_tree_nodes.append(["R",list(),list()])
            i = i+1
        elif formula_str[i] == 'W':
            op_idxs.append('W') 
            paren_map.append(paren_level)
            operator_strength.append(1)
            empty_tree_nodes.append(["W",list(),list()])
            i = i+1
        elif formula_str[i] == 'M':
            op_idxs.append('M') 
            paren_map.append(paren_level)
            operator_strength.append(1)
            empty_tree_nodes.append(["M",list(),list()])
            i = i+1
            
        # Unary operators:
        elif formula_str[i] == 'X':
            op_idxs.append('X') 
            paren_map.append(paren_level)
            operator_strength.append(2)
            empty_tree_nodes.append(["X",list()])
            i = i+1
        elif formula_str[i] == 'F':
            op_idxs.append('F') 
            paren_map.append(paren_level)
            operator_strength.append(2)
            empty_tree_nodes.append(["F",list()])
            i = i+1
        elif formula_str[i] == 'G':
            op_idxs.append('G') 
            paren_map.append(paren_level)
            operator_strength.append(2)
            empty_tree_nodes.append(["G",list()])
            i = i+1
        # 'neg' with parentheses or spaces:
        elif formula_str[i:i+3] in ['neg','not','NEG','NOT','Neg','Not'] and formula_str[i-1] in [')',' '] and formula_str[i+3] in ['(',' ']:
            op_idxs.append('neg')
            paren_map.append(paren_level)
            operator_strength.append(2)
            empty_tree_nodes.append(["neg",list()])
            i = i+3
        
        # eliminate parentheses, but map them: 
        elif formula_str[i] == '(':
            paren_level = paren_level + 1
            i = i+1
        elif formula_str[i] == ')':
            paren_level = paren_level - 1
            i = i+1
            
        # Finally, handle atoms:    
        elif formula_str[i] != ' ':
            # we encounter a character which is neither a space nor an operator (atom!)
            atom = ''.join([atom, formula_str[i]])
            
            if formula_str[i+1] in [' ', 'U', 'R', 'W', 'M', 'X', 'F', 'G', '(', ')','-']:
                # we've reached the end of the atom
                op_idxs.append(atom)
                label_list.append(atom)
                paren_map.append(paren_level)
                operator_strength.append(-1)
                empty_tree_nodes.append(["AP",[atom]])
                atom = ''
                
            i = i+1

        else:
            # We just have an uninteresting space.
            i = i + 1
                
        index_dict = dict()
        index_dict['op_idxs'] = op_idxs
        index_dict['paren_map'] = paren_map
        index_dict['operator_strength'] = operator_strength
        index_dict['empty_tree_nodes'] = empty_tree_nodes
        index_dict['label_list'] = label_list
        
    return index_dict

def populate_node(node_dict):
    # Flag for if we've reached a leaf:
    is_leaf = False
    node = list()
    
    formula_indexed = node_dict['op_idxs']
    paren_map = node_dict['paren_map']
    operator_strength = node_dict['operator_strength']
    empty_tree_nodes = node_dict['empty_tree_nodes'] 
    
    num_elements = len(formula_indexed)
    
    # Check if the provided argument is a leaf:
    if len(operator_strength) == 1 and operator_strength[0] == -1:
        is_leaf = True       
        args_list = []
        node = empty_tree_nodes[0]

        return node, args_list, is_leaf
    
    # Move through formula segment by operator strength and 
    # parenthetical level until weakest is found:
    
    break_loops = False

    for i in range(0, max(paren_map)+1): # parenthetical level

        for j in range(0,3): # operator strength

            for idx in range(0, num_elements): # position in indexed formula segment
                
                if paren_map[idx] == i and operator_strength[idx] == j:
                    node = empty_tree_nodes[idx]
                    break_loops = True
                    break
            if break_loops:
                break
        if break_loops:
            break
    
    args_list = list()
    left_arg = dict()
    right_arg = dict()
    
    if len(node) == 3: # two-argument operator
        
        # Split all strings into the two arguments of the operator
        left_arg['op_idxs'] = formula_indexed[0:idx]
        left_arg['paren_map'] = paren_map[0:idx]
        left_arg['operator_strength'] = operator_strength[0:idx]
        left_arg['empty_tree_nodes'] = empty_tree_nodes[0:idx]
        
        right_arg['op_idxs'] = formula_indexed[idx+1:num_elements]
        right_arg['paren_map'] = paren_map[idx+1:num_elements]
        right_arg['operator_strength'] = operator_strength[idx+1:num_elements]
        right_arg['empty_tree_nodes'] = empty_tree_nodes[idx+1:num_elements]
        
        args_list = [left_arg, right_arg]
        
    elif len(node) == 2: # one-argument operator            
        
        right_arg['op_idxs'] = formula_indexed[idx+1:num_elements]
        right_arg['paren_map'] = paren_map[idx+1:num_elements]
        right_arg['operator_strength'] = operator_strength[idx+1:num_elements]
        right_arg['empty_tree_nodes'] = empty_tree_nodes[idx+1:num_elements]    
            
        args_list = [right_arg]   
            
            
    return node, args_list, is_leaf

def nest_nodes(node_dict):
    node, args_list, is_leaf = populate_node(node_dict)
    
    if is_leaf:
        pass
        
    elif len(args_list) == 1:
        node[1] = nest_nodes(args_list[0])
        
    elif len(args_list) == 2:

        node[1] = nest_nodes(args_list[0])
        node[2] = nest_nodes(args_list[1])
        
    return node

def dump_trees_json(trees, test_name='default'):
    
    config_path = f'./test_tree_making/{test_name}.json'
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)

    # Populate file
    with open(config_path, 'w') as f:
        json.dump(obj=trees, fp = f, indent = 4)
        
        
def parse_formula(formula_str):
    
    index_dict = index_formula(formula_str)
    label_list = index_dict['label_list']
    
    # formula_indexed = index_dict['op_idxs']
    # paren_map = index_dict['paren_map']
    # operator_strength = index_dict['operator_strength']
    # empty_tree_nodes = index_dict['empty_tree_nodes']
    
    # Recursively generate trees from indexed formula
    # (big oof)
    full_tree = list()
    
    full_tree = nest_nodes(index_dict)
    
    
    return full_tree


def test_formula_parser(form_strs):
    trees = dict()
    trees['formula_trees'] = list()
    
    for rule in form_strs:
        tree = parse_formula(rule)
        trees['formula_trees'].append(tree)
    
    #dump_trees_json(trees)
    #print(trees)
    pass


if __name__ == '__main__':
    
    rule_strings = [
        
        'GX1 -> (2 or 3 U 4)',
        'a -> bUc -> Xd',
        'f AND (apple ->b U (cat_box->d)) ->eggs'
    ]
    
    test_formula_parser(rule_strings)
    
    
    