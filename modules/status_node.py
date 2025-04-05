import numpy as np

#######################################################
# RuleNode: object representing one node in a rule tree
#######################################################

class RuleNode:
    def __init__(self, node_id, optype):
        # Rule Node ID Information
        self.id = node_id # node_id will be a list of strings, e.g. ['1','0','1'] 
        self.id_string = ".".join(node_id) # .id_string is id as string: e.g. '1.0.1'
        self.no = int(node_id[-1]) # integer node no 
        
        # Rule Node Properties
        self.optype = optype # optype will be LTL operator type as a str
        
        # Rule Node Positioning in Tree and Contents
        self.parent = list() # list containing the parent StatusNode object
        self.children = list() # list containing the child StatusNode object(s)
        self.label = '' # contains a label if node is a leaf
        if optype == 'AP':
            self.is_leaf = True
        else:
            self.is_leaf = False
        
        
        # a RuleNode will be associated with status data for each trace segment via a corresponding StatusNode. 
        
    def get_children(self):
        return self.children
    def get_parent(self):
        return self.parent
    
#######################################################
# RuleTree: object containing all the nodes of a single LTL rule
#######################################################
        
class RuleTree:
    def __init__(self, tree_id):
        # Tree ID Information
        tree_id_str = str(tree_id)
        self.id = [tree_id_str]
        self.id_string = tree_id_str
        
        # Tree Structuring Information
        self.labels = list() # list of labels appearing in formula
        self.nodes = dict()
        self.leaves = list()
        
        # Population order information (optional)
        self.pop_order = list()
        
    def set_pop_order(self, pop_order):
        self.pop_order = pop_order
    
    def add_child_node(self, parent_node : RuleNode, optype, label=''):
        child_list = parent_node.get_children()
        if len(child_list) > 0:
            last_child = child_list[-1] # get last child if exists
            last_child_no = last_child.no
        else:
            last_child_no = -1 # start index at 0
        new_child_no = last_child_no + 1 # increment id number by one
        
        parent_id = parent_node.id
        new_child_id = parent_id + [str(new_child_no)] # create child ID 
        child_node = RuleNode(new_child_id, optype) # create child
        
        child_node.parent = [parent_node] # add parent node to property of child node
        parent_node.children.append(child_node) # add child node to property of parent node
        
        if child_node.is_leaf:
            child_node = self.add_leaf_node(child_node, label)
        
        # Add new node to tree:
        new_child_id_str = child_node.id_string
        self.nodes[new_child_id_str] = child_node
        # Return new child node object
        return child_node
    
    def add_leaf_node(self, leaf : RuleNode, label):

        # Leaf node handling (add label attribute)
        leaf.label = label
        self.leaves.append(leaf)
        if label not in self.labels:
            self.labels.append(label)
        return leaf
    
    def make_trunk(self, optype, label=None):
        node_id = self.id
        first_node = RuleNode(node_id, optype) # create first node in tree (trunk)
        self.nodes[first_node.id_string] = first_node
        
        if first_node.is_leaf:
            first_node = self.add_leaf_node(first_node, label)
 
        # Return new node in case we need it
        return first_node
        
    
    def add_parent_node(self, child_id):
        pass
    
#######################################################
# StatusNode: object containing the status data for one node given an individual trace
#######################################################

class StatusNode:
    def __init__(self, rule_node : RuleNode, trace_id, trace):
        # Trace Information
        self.trace_id = str(trace_id) # id number given to trace
        self.trace = trace # trace (as list of lists), e.g. [['a'], ['a','b'], []]
        trace_len = len(trace)
        self.trace_length =  trace_len
        
        # Rule Node Information
        self.id = rule_node.id # node_id matches id of corresponding RuleNode
        self.id_string = rule_node.id_string # ""
        self.optype = rule_node.optype
        self.populated = False
        
        # Status and Formula Truth Data (to be evaluated for individual segments \rho^{t_0...})
        self.tau_a_list = list() 
        self.tau_s_list = list() # tau_q_list[i] will contain list tau_q for \rho^{i...}
        self.tau_i_list = list()
        self.tau_v_list = list()
        self.true_at_t0 = list()
        # Extra information for signature
        self.t_s_list = list()
        self.child_info = list()
        self.check_sustain_at_ts = 1
        
#######################################################
# LiveNode: object containing the LIVE status data for one node given an individual trace
#######################################################

class LiveNode:
    def __init__(self, rule_node : RuleNode, trace_id, trace):
        # Trace Information
        self.trace_id = str(trace_id) # id number given to trace
        self.trace = trace # trace (as list of lists), e.g. [['a'], ['a','b'], []]
        trace_len = len(trace)
        self.trace_length =  trace_len
        # Indicate whether the current segment is the full trace
        self.end_trace = False
        
        # Rule Node Information
        self.id = rule_node.id # node_id matches id of corresponding RuleNode
        self.id_string = rule_node.id_string # ""
        self.optype = rule_node.optype
        self.populated = False
        
        # Live status of node for each t0 in partial trace 
        self.node_status_for_t0 = list() 
        # Separate into binary vectors:
        # (only need to use this for some modules)
        self.true_at_t0 = list()
        self.false_at_t0 = list()
        
        # Same data but separated out into 3 lists of indices (to be evaluated for individual segments \rho^{t_0...})
        #self.true_idx_list = list() 
        #self.false_idx_list = list() 
        #self.open_idx_list = list()
        
        # Update information:
        # Store indices of info that was updated on this pass (everything else stayed the same)
        self.updated_idxs = list()
        
        self.update_history = list()
        # Info can be used for extra update information etc. as necessary for each node.
        self.info = -1

        # Extra information for signature (may not be necessary)
        #self.t_s_list = list()
        #self.child_info = list()
        #self.check_sustain_at_ts = 1
    
    def trace_update(self, new_trace, end_trace):
        self.trace = new_trace
        self.trace_length = len(new_trace)
        self.end_trace = end_trace
        
    def update_history_update(self, updates):
        self.update_history.append(updates)
    
def test_status_node():
    op_type_test = 'U'
    tree_id = 2 #can be given as int or string (will be converted to str)
    labels = ['a', 'b', 'c']
    
    tree_two = RuleTree(tree_id, labels)
    #print('tree id: ', tree_two.id)
    #print('tree labels: ', tree_two.labels)
    tree_two.make_first_node(op_type_test)
    first_node = tree_two.nodes['2']
    #print('First node type:', first_node.optype)
    
    # Add a first child node
    child = tree_two.add_child_node(first_node, 'X')
    #print('First child id: ', child.id)
    
    pass
    
if __name__ == '__main__':
    
    test_status_node()