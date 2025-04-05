from pathlib import Path
import sys
import os

for i in range(5):
    if not (Path.cwd()/"modules").exists(): os.chdir(Path.cwd().parent.as_posix())
    else: sys.path.append(Path.cwd().as_posix())

import modules.status_node as sn
import assess_rule_status as ars
import build_tree as bt
import parse_formula as pf

class nodeSignature:
     def __init__(self, status_node : sn.StatusNode):

        # Node and trace information:
        self.trace_id = status_node.trace_id # id number given to trace
        self.node_id = status_node.id
        self.node_id_string = status_node.id_string
        
        # Signature information
        self.node_signature = list()
        # Information about what to check for child nodes
        self.sustain_node_idx = -1
        self.sus_spans = list()
        self.release_node_idx = -1
        self.rel_spans = list()
        

def get_node_signature(status_node : sn.StatusNode, timespan_list):
    node_id_str = status_node.id_string

    # Instantiate node signature object
    node_signature = nodeSignature(status_node)
    
    signature = list()
    print(f'Getting signature for Node {node_id_str}')

    child_info = status_node.child_info # Child info format: [int, int]
    sustain_arg_idx = child_info[0] # will be 0 if 1st arg is sustain criterion, 1 if 2nd arg, and -1 if there is no sustain criterion.
    release_arg_idx = child_info[1] # will be 0 if 1st arg is release criterion, ... (see above)
    # note: for AP nodes (leaves), child_info is [-1, -1]
    check_sus_at_ts = status_node.check_sustain_at_ts # check whether operator type requires sustain criterion true at t_s
    
    # Will track which types of arguments we have
    sus_arg = False
    rel_arg = False
    # Get IDs of sustain and release child nodes
    if sustain_arg_idx >= 0:
        node_signature.sustain_node_idx = sustain_arg_idx
        sus_arg = True
    if release_arg_idx >= 0:
        node_signature.release_node_idx = release_arg_idx
        rel_arg = True
        
    # Begin moving through timespans for this node.
    t0 = 0
    t0_checked_for_children = -1
    
    for timespan in timespan_list:
        print("**************************")
        print("**************************")
        t0_min = timespan[0]
        t0_max = timespan[-1] # Handles singleton set time spans
        #span_status_info = [None] * (t0_max+1 - t0_min)
        print('timespan is: ', timespan)
        #print('span_status_info is: ', span_status_info)
        
        # Each node will have a "signature" consisting of a list of signature elements.
        # These elements will have format [t_min, t_max, 'q'] where t_min is start of a time span, 
        #   t_max is last time (incl),
        #   and 'q' is status of the node on \rho^{t_0...}, t=t_0 for each t_0 in [t_min, t_max]. 
        signature_element = list()
        
        t0 = t0_min
        
        # Flags to keep track of status changes across time steps
        inactive = False
        violated = False
            
        while t0 <= t0_max:
            # if node is active at t0, t=t0:
            if status_node.tau_a_list[t0][0] == 1:
                inactive = False
                violated = False
                # Get satisfaction time
                t_s = status_node.t_s_list[t0]
                print("*************************************")
                print('t0 is: ', t0)
                print('tau_a is: ', status_node.tau_a_list[t0])
                print('t_s is: ', t_s)
                
                # Add relevant t0s to child timespans of interest
                if t0 > t0_checked_for_children:
                    if sus_arg:
                        # check_sus_at_ts = 1 if we need to include a check of the sustain criterion at ts
                        sus_timespan = [t0, t_s + check_sus_at_ts - 1] #
                        # if the rule is satisfied at t=0 and doesn't require sustain at t_s, it's a special case.
                        if t_s + check_sus_at_ts - 1 >= 0:
                            print('sus timespan: ', sus_timespan)
                            node_signature.sus_spans.append(sus_timespan)
                        
                    if rel_arg:
                        # need to check the release criterion at t_s
                        rel_timespan = [t_s]
                        print('rel timespan is: ', rel_timespan)
                        node_signature.rel_spans.append(rel_timespan)
                
                if t_s <= t0_max:
                    #span_status_info[t0-t0_min:t_s+1-t0_min] = ['a']*(t_s+1-t0) #note active statuses
                    # Add active span to signature
                    signature_element = [t0,t_s,'a']
                    signature.append(signature_element)
                    signature_element = []
                    print('ts + 1 - t0: ', t_s+1-t0)
                    t0 = t_s + 1
                else:
                    #span_status_info[t0-t0_min:t0_max+1-t0_min] = ['a']*(t0_max+1-t0)
                    signature_element = [t0, t0_max, 'a']
                    signature.append(signature_element)
                    signature_element = []
                    print('t0_max + 1 - t0: ', t0_max+1-t0)
                    t0 = t0_max + 1
                    
                t0_checked_for_children = t_s
                
            # Implication node that is not "triggered" (inactive from t0)    
            elif status_node.tau_i_list[t0][0] == 1:
                #span_status_info[t0-t0_min] = 'i'
                
                # if previous timestep was also inactive, we update the existing element
                if inactive: 
                    signature_element[1] = t0
                else: # this is the first timestep that is inactive
                    # If the previous element wasn't added yet, add to signature (and make a new one)
                    if len(signature_element) > 0:
                        signature.append(signature_element)
                    signature_element = [t0, t0, 'i']
                    inactive = True
                    violated = False
                t0_checked_for_children = t0
                t0 = t0 + 1
                
            else: # means node is violated on \rho^{t_0...}
                if violated: 
                    signature_element[1] = t0
                else: # this is the first timestep that is violated
                    # If the previous element wasn't added yet, add to signature (and make a new one)
                    if len(signature_element) > 0:
                        signature.append(signature_element)
                    signature_element = [t0, t0, 'v']
                    inactive = False
                    violated = True
                t0_checked_for_children = t0
                t0 = t0 + 1    
        # If the final element wasn't added yet, add to signature (and clear it)
        if len(signature_element) > 0:
            signature.append(signature_element) 
            signature_element = []           
        
    node_signature.node_signature =  signature
    
    return node_signature

def get_signature(status_nodes_dict, node_signatures_dict, rule_tree : sn.RuleTree, node_id_str = None, timespan_list = None, make_leaf_signatures = False):
    
    if timespan_list is None:
        timespan_list = [[0]]
    if node_id_str is None:
        node_id_str = rule_tree.id_string
        
    rule_node = rule_tree.nodes[node_id_str]
    status_node = status_nodes_dict[node_id_str]
    
    node_op_type = rule_node.optype
    
    if not make_leaf_signatures and node_op_type == 'AP':
        return node_signatures_dict
        
    node_signature = get_node_signature(status_node, timespan_list)
    
    # Enter node signature into dictionary of node signatures
    node_signatures_dict[node_id_str] = node_signature

    # Information about what to check for child nodes
    child_nodes = rule_node.children
    sus_node_idx = node_signature.sustain_node_idx
    rel_node_idx = node_signature.release_node_idx
    
    if sus_node_idx > -1:
        # Identify corresponding rule and status nodes
        sustain_rule_node = child_nodes[sus_node_idx]
        sus_node_id_str = sustain_rule_node.id_string
        print(f'sus node id string: {sus_node_id_str}')
        # Get timespans
        sustain_timespans = node_signature.sus_spans
        node_signatures_dict = get_signature(status_nodes_dict, node_signatures_dict, rule_tree, node_id_str=sus_node_id_str, timespan_list=sustain_timespans)
    
    if rel_node_idx > -1:
        # Identify corresponding rule and status nodes
        release_rule_node = child_nodes[rel_node_idx]
        rel_node_id_str = release_rule_node.id_string
        print(f'rel node id string: {rel_node_id_str}')
        # Get timespans
        release_timespans = node_signature.rel_spans
        node_signatures_dict = get_signature(status_nodes_dict, node_signatures_dict, rule_tree, node_id_str = rel_node_id_str, timespan_list = release_timespans)
        
    return node_signatures_dict

def test_signatures():
    #           '0'      '1'    '2'    '3'         '4'      '5'      '6'    '7'
    trace = [['a'], ['a'], ['a'], ['a'], ['a','b'], ['a'], ['a'], ['a']]
    
    #trace = [['a','b'], ['a'], ['a'], ['a'], ['a'], ['a'], ['a']]
    trace_id = 0
    tree_id = 2
    formula = "a U b"

    formula_parsed = pf.parse_formula(formula)
    rule_tree = bt.build_tree(formula_parsed, tree_id)
    status_nodes_dict = ars.assess_rule_status(trace, rule_tree, trace_id) 
    
    node_signatures_dict = dict()
    
    node_signatures_dict = get_signature(status_nodes_dict, node_signatures_dict, rule_tree)
    
    node_ids = node_signatures_dict.keys()
    for key in node_ids:
        print(f'Signature for node {key}')
        print(node_signatures_dict[key].node_signature)
    pass
        
        

if __name__ == '__main__':
    test_signatures()