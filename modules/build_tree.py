import modules.parse_formula as pf
import modules.status_node as sn
import numpy as np

####################################################
# Tree Building script
####################################################
# Noel Brindise, Sept 2024
#
# Purpose: convert LTL formula trees (in list format) into a RuleTree object
# Input: list
# Output: formula tree as a RuleTree
#
# Howto: 
# 
#   Call build_tree() for a nested list of strings (see parse_formula.py)
#   ex1) build_tree(parse_formula('dog U (cat and frog)'))
#
#  

####################################################
# 
####################################################

def build_tree(formula, tree_id): 
    
    tree = sn.RuleTree(tree_id)
    #print('tree id: ', tree.id)
    
    # Iterate through the nested lists created by parse_formula
    # Iteration begins at top level ('trunk') and progresses down to leaves
    # List format is as follows:
    # ['operator type', ['arg_0 operator type', [... ['label']]], ['arg_1 op type', [...['label']]]]
    # e.g.
    # ['U', ['AP', ['a']], ['F', ['AP', ['b']]]] for a U Fb
    
    tree = populate(formula, tree)
    node_names = tree.nodes.keys()
    for name in node_names:
        #print('name: ', name)
        node = tree.nodes[name]
        optype = node.optype
        #print('optype: ', optype)
    return tree
    
def populate(value, tree : sn.RuleTree, current_parent=None):

    optype = value[0]
    if optype == 'AP': # leaf
        arg0 = value[1] # list containing label string
        label = arg0[0]
        if current_parent is None: # leaf is also first (and only) node!
            tree.make_trunk(optype, label) 
            return tree
        else: # normal leaf
            tree.add_child_node(current_parent, optype, label)
            return tree
    else: # not leaf
        if current_parent is None: # this is first (and only) node!
            new_node = tree.make_trunk(optype) 
        else: # this is a normal node
            new_node = tree.add_child_node(current_parent, optype)
        current_parent = new_node
        for i in range(1, len(value)): # Iterate through node arguments
            arg = value[i]
            tree = populate(arg, tree, current_parent)                
            
    return tree
        
    
    
def test_build_tree():
    formula_str = "F b and (a U c)"
    parsed_formula, labels = pf.parse_formula(formula_str)
    tree_id = 2
    tree = build_tree(parsed_formula, tree_id)
    
    node_names = tree.nodes.keys()
    for name in node_names:
        #print('name: ', name)
        node = tree.nodes[name]
        optype = node.optype
        #print('optype: ', optype)
        isleaf = node.is_leaf
        #print('isleaf: ', isleaf)
        #print('label: ', node.label)
        parent_list = node.parent
        if len(parent_list)>0:
            parent = parent_list[0]
            #print('parent id: ', parent.id_string)
        children_list = node.children
        if len(children_list)>0:
            for child in children_list:
                #print('child id: ', child.id_string)
                pass
        
    print(node_names)
    
    return tree
    
    
if __name__ == '__main__':
    
    print(test_build_tree())