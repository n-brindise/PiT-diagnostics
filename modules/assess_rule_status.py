import modules.status_node as sn
import modules.operator_modules as om
import numpy as np

####################################################
# Rule status assessment for trace
####################################################
# Noel Brindise, Sept 2024
#
# Purpose: 
# Input: 
# Output: 
#
# Howto: 
# 
#   Call 
#
#  
####################################################
# 
####################################################

#######################################################
# Function instantiate_status_nodes: 
#   build dict of status nodes corresponding to rule nodes in tree
#######################################################

def instantiate_status_nodes(trace, tree : sn.RuleTree, trace_id):
    
    status_nodes_dict = dict()
    
    rule_node_dict = tree.nodes # Get dictionary containing all rule nodes in tree
    rule_node_ids = rule_node_dict.keys() # Get the node IDs
    
    # For each rule node, create a corresponding status node
    for node_id in rule_node_ids:
        rule_node = rule_node_dict[node_id]
        status_nodes_dict[node_id] = sn.StatusNode(rule_node, trace_id, trace)       
    
    # Return the status nodes as a dict
    return status_nodes_dict

def populate_status_node(status_node : sn.StatusNode, t0_truth_data, T_0):

    status_node = om.to_module(status_node, t0_truth_data, T_0)
    
    status_node.populated = True
    return status_node


def assess_rule_status(trace, tree : sn.RuleTree, trace_id=0):
    # Create status nodes for this trace given a rule tree
    status_nodes_dict = instantiate_status_nodes(trace, tree, trace_id)
    
    # Start with leaves and build up for status assessment.
    # We will only do the evaluation once per label, since leaves with the same
    #   label will have the exact same status data.
    labels = tree.labels
    generic_label_nodes = dict()
    
    for label in labels:
        # Instantiate a generic status node for each label...
        generic_leaf_node = sn.RuleNode(['99','99'], 'AP')
        generic_status_node = sn.StatusNode(generic_leaf_node, trace_id, trace)

        generic_status_node = om.ap_module(label, generic_status_node)
            
        generic_label_nodes[label] = generic_status_node
        
    # Now assign correct values to each leaf in RuleTree.
    #print('tree leaves: ', tree.leaves)
    
    for leaf in tree.leaves:
        current_label = leaf.label
        node_id_string = leaf.id_string
        generic_node = generic_label_nodes[current_label]
        status_node = status_nodes_dict[node_id_string]
        status_node.tau_a_list = generic_node.tau_a_list
        status_node.tau_s_list = generic_node.tau_s_list 
        status_node.tau_i_list = generic_node.tau_i_list 
        status_node.tau_v_list = generic_node.tau_v_list
        status_node.true_at_t0 = generic_node.true_at_t0 
        status_node.t_s_list = generic_node.t_s_list
        status_node.child_info = generic_node.child_info
        status_node.check_sustain_at_ts = generic_node.check_sustain_at_ts
        
        status_node.populated = True
        
        # test_node = status_nodes_dict[node_id_string]
        # print('test status (does status_nodes_dict update?): ', test_node.populated)
        
        #print(f'status node {node_id_string} for {current_label}:')
        #print(f'tau_a list: {status_node.tau_a_list}')
        #print(f'tau_s list: {status_node.tau_s_list}')
        #print(f'tau_i list: {status_node.tau_i_list}')
        #print(f'tau_v list: {status_node.tau_v_list}')
        #print(f'true at t0: {status_node.true_at_t0}')
        
    ########################
    # Now work up tree by instantiating parent nodes
    
    for leaf in tree.leaves:
        #node_id_string = leaf.id_string
        if len(leaf.parent) < 1: # If formula is just one label
            print('just one label')
            break
        parent = leaf.parent[0] # Get parent rule node of current leaf
        unpopulated_child = False
        
        # If all children are populated, we can assess the parent.
        # If parent is already populated, no need to do it again.

        unpopulated_child = False
        children_to_check = parent.children
        for child in children_to_check:
            status_child_node = status_nodes_dict[child.id_string]
            if not status_child_node.populated:
                unpopulated_child = True
        
        
        # Begin working up the tree...
        while not unpopulated_child:
            # Get current parent node information
            optype = parent.optype
            parent_id_str = parent.id_string
            parent_status_node = status_nodes_dict[parent_id_str]
            
            # Only populate the parent node if it hasn't already been done
            if not parent_status_node.populated:
            
                # Get truth data from children
                children = parent.children # Get all RuleNode children of current parent
                #print(f"Children: {children}")
                #print(f"len(Children): {len(children)}")
                t0_truth_data = [None] * len(children)
                for child in children:
                    child_no = child.no
                    child_id_str = child.id_string
                    # Get child status data
                    child_status_node = status_nodes_dict[child_id_str]
                    # Place data in correct argument position in list
                    #print(f"putting child node {child_id_str} in position {child_no}")
                    #print(f"info: {child_status_node.true_at_t0}")
                    t0_truth_data[child_no] = child_status_node.true_at_t0
                    
                # Populate the parent status node
                T_0 = 0
                populated_node = populate_status_node(parent_status_node, t0_truth_data, T_0)
            
            # Now attempt to move up to parent of parent:
            if len(parent.parent) > 0: # make sure we haven't reached the top yet
                new_parent = parent.parent[0]
                children = new_parent.children # Get all children of that parent
                unpopulated_child = False
                # Loop through each child RuleNode
                for child in children: 
                    child_id_str = child.id_string
                    # Get corresponding status node
                    child_status_node = status_nodes_dict[child_id_str]
                    # If one hasn't been populated, we need to move to next leaf
                    if not child_status_node.populated:
                        unpopulated_child = True
                
                parent = new_parent    
            else:
                break
    # Do a population check...
    for rule_node_id in tree.nodes.keys():
        status_node = status_nodes_dict[rule_node_id]
        #print(status_node.populated)
        
    return status_nodes_dict
        
    