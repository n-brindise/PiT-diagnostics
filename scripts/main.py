from pathlib import Path
import os
import sys
import numpy as np

print('current directory: ', Path.cwd())
#import modules
for i in range(5):
    if not (Path.cwd()/"modules").exists(): os.chdir(Path.cwd().parent.as_posix())
    else: sys.path.append(Path.cwd().as_posix())
    
print('current directory: ', Path.cwd())

import modules.status_node as sn
import modules.build_tree as bt
import modules.assess_rule_status as ars
import modules.parse_formula as pf
import modules.interactive_rsa as ir
#import modules.trace_characterization as tc
#import modules.assess_live_status as als

def run_interactive_expl(tree_id, status_nodes_dict, t, depth):
    
    return ir.get_expl_at_t(tree_id, status_nodes_dict, t, depth)

def test_status_alg():
    trace = [['a','b'], ['a'], [''], ['a'], ['a'], ['b'], ['b']]
    #trace = [['a'], ['a'], ['a'], ['a'], ['a','c'], ['a'], ['a','b']]
    trace_id = 0
    tree_id = 2
    formula = "a U (F b)"

    formula_parsed = pf.parse_formula(formula)
    rule_tree = bt.build_tree(formula_parsed, tree_id)
    status_nodes_dict = ars.assess_rule_status(trace, rule_tree, trace_id)     
    
    print(f"Nodes available: {status_nodes_dict.keys()}")
    # for key in status_nodes_dict.keys():
    #     status_node = status_nodes_dict[key]
    #     print(f"Node: {key}")
    #     #print(f"T0 truth times: {status_node.true_at_t0}")
    #     # for tau_a in status_node.tau_a_list:
    #     #     print(f"tau_a: {tau_a}")
    #     # for tau_s in status_node.tau_s_list:
    #     #     print(f"tau_s: {tau_s}")
    #     # for tau_i in status_node.tau_i_list:
    #     #     print(f"tau_i: {tau_i}")
    #     # for tau_v in status_node.tau_v_list:
    #     #     print(f"tau_v: {tau_v}")
    
    # Test explanations / diagnostics
    
    
    #run_interactive_expl(tree_id, status_nodes_dict, t, depth)
    
    #tc.get_signature(tree_id, status_nodes_dict, rule_tree)
    
    pass


    

if __name__ == '__main__':
    
    test_status_alg()
    # Live tracking values not yet supported
    #test_live_status()
