import modules.status_node as sn 
import numpy as np


####################################################
# Rule status assessment modules
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
####################################################
# 
####################################################

def to_module(status_node : sn.StatusNode, t0_truth_data, t0):
    optype = status_node.optype
    
    if optype == 'or':
        status_node = or_module(status_node, t0_truth_data, t0)
    elif optype == 'and':
        status_node = and_module(status_node, t0_truth_data, t0)
    elif optype == 'neg': 
        status_node = not_module(status_node, t0_truth_data, t0)
    elif optype == '->':
        status_node = implies_module(status_node, t0_truth_data, t0)
    elif optype == 'G':
        status_node = global_module(status_node, t0_truth_data, t0)
    elif optype == 'F':
        status_node = eventually_module(status_node, t0_truth_data, t0)
    elif optype == 'X':
        status_node = next_module(status_node, t0_truth_data, t0)
    elif optype == 'U': 
        status_node = until_module(status_node, t0_truth_data, t0)
    elif optype == 'R':
        status_node = release_module(status_node, t0_truth_data, t0)
    elif optype == 'W':
        status_node = weak_until_module(status_node, t0_truth_data, t0)
    elif optype == 'M':
        status_node = strong_release_module(status_node, t0_truth_data, t0)
    else:
        print(f'type: {optype}')
        print('Error in formula parsing (Operator type not recognized)')

    return status_node

####################################
# AP Module
####################################

def ap_module(label, status_node : sn.StatusNode):
    trace = status_node.trace
    T_f= len(trace)
    child_info = [-1, -1] # no children
    status_node.child_info = child_info
    #print(f'node id: {status_node.id_string}')
    status_node.check_sustain_at_ts = 0
    
    for t0 in range(0, T_f):
    
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
        
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
    
        true_at_t0 = False
        
        if label in trace[t0]: # e.g. if 'a' in ['a', 'c']
            true_at_t0 = True
            tau_a[0] = 1
            tau_s[0] = 1
            t_s = t0
            tau_i = tau_i - tau_a
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
            
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)

        
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    #print('status_node.child_info:', status_node.child_info)
    return status_node
           
    

#####################################################
# LOGICAL OPERATORS
#####################################################

####################################
# or Module 'or'
####################################

def or_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    T_f = len(trace)
    child_info = [0, 1] # doesn't matter which arg is release and which is sustain.
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 1
    
    for t0 in range (T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
    
        true_at_t0 = False
        
        # Get child truth information
        arg0_true = t0_truth_data[0][t0]
        arg1_true = t0_truth_data[1][t0]
        
        if arg0_true or arg1_true:
            true_at_t0 = True
            tau_a[0] = 1
            tau_s[0] = 1
            t_s = t0
            tau_i = tau_i - tau_a
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node

####################################
# and Module 'and'
####################################

def and_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    
    trace = status_node.trace
    T_f = len(trace)
    child_info = [0, 1] # doesn't matter which arg is release and which is sustain.
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 1
    
    for t0 in range (T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
    
        true_at_t0 = False
        
        # Get child truth information
        arg0_true = t0_truth_data[0][t0]
        arg1_true = t0_truth_data[1][t0]
        
        if arg0_true and arg1_true:
            true_at_t0 = True
            tau_a[0] = 1
            tau_s[0] = 1
            t_s = t0
            tau_i = tau_i - tau_a
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node
###################################
# not Module 'neg'
####################################

def not_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    T_f = len(trace)
    child_info = [-1, 0] # no sustain; first arg is release
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 0
    
    for t0 in range (T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
    
        true_at_t0 = False
        
        # Get child truth information
        arg0_true = t0_truth_data[0][t0]
        
        if not arg0_true:
            true_at_t0 = True
            tau_a[0] = 1
            tau_s[0] = 1
            t_s = t0
            tau_i = tau_i - tau_a
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node

####################################
# implies Module '->'
####################################

def implies_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    T_f = len(trace)
    child_info = [0, 1] # call the trigger argument the sustain.
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 1 # If active, both first and second arg must be true at t0

    for t0 in range (T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
    
        true_at_t0 = False
        
        # Get child truth information
        arg0_true = t0_truth_data[0][t0]
        arg1_true = t0_truth_data[1][t0]
        
        if not arg0_true: #tau_v_0 not empty
            true_at_t0 = True
        elif not arg1_true: 
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
        else:
            true_at_t0 = True
            tau_a[0] = 1
            tau_s[0] = 1
            t_s = t0
            tau_i = tau_i - tau_a
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node

#####################################################
# TEMPORAL OPERATORS
#####################################################

####################################
# Global (G) Module 'G'
####################################

def global_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    child_info = [0, -1] # Sustain first argument; no release criterion
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 1
    T_f = len(trace)
    
    for t0 in range(T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
    
        true_at_t0 = False
        
        for t_test in range(t0, T_f):
            # Get child truth information
            arg0_true = t0_truth_data[0][t_test]
            if not arg0_true: #tau_v_0 nonempty
                break
            
        if arg0_true:
            tau_a = np.ones(T_f-t0)
            tau_s[-1] = 1
            t_s = T_f - 1
            tau_i = tau_i - tau_a
            true_at_t0 = True
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node

####################################
# Next (X) Module 'X'
####################################

def next_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    T_f = len(trace)
    child_info = [-1, 0] # No sustain criterion; first argument is release criterion
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 0
    
    for t0 in range (T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
        
        # Store additional info to produce "signature" later.
        t_s = -1
        
    
        true_at_t0 = False
        
        if t0+1 < T_f:
            # Get child truth information
            arg0_true = t0_truth_data[0][t0+1]
        else:
            arg0_true = False
        
        if arg0_true: #tau_v_0 empty
            tau_a[0] = 1
            tau_a[1] = 1
            tau_s[1] = 1
            t_s = t0+1
            tau_i = tau_i - tau_a
            true_at_t0 = True
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node
####################################
# Eventually (F) Module 'F'
####################################

def eventually_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    T_f = len(trace)
    child_info = [-1, 0] # no sustain criterion; first argument is release criterion
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 0
    
    for t0 in range(T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
    
        true_at_t0 = False
        
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
        
        for t_test in range(t0, T_f):
            # Get child truth information
            arg0_true = t0_truth_data[0][t_test]
            if arg0_true: #tau_v_0 empty
                break
            
        
        if arg0_true:
            true_at_t0 = True
            tau_a[0:t_test-t0+1] = np.ones(t_test-t0+1)
            tau_s[t_test-t0] = 1
            t_s = t_test
            tau_i = tau_i - tau_a
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
        
    return status_node

####################################
# Until (U) Module 'U'
####################################

def until_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    T_f = len(trace)
    child_info = [0, 1] # first arg is sustain criterion; second argument is release criterion
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 0
    
    for t0 in range(T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
    
        true_at_t0 = False

        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
        
        for t_test in range(t0, T_f):
            # Get child truth information
            arg0_true = t0_truth_data[0][t_test]
            arg1_true = t0_truth_data[1][t_test]
            if arg1_true or not arg0_true:
                break
            
        if arg1_true: #tau_v_1 empty
            true_at_t0 = True
            tau_a[0:t_test-t0+1] = np.ones(t_test-t0+1)
            tau_s[t_test-t0] = 1
            t_s = t_test
            tau_i = tau_i - tau_a
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node
####################################
# Weak Until (W) Module 'W'
####################################

def weak_until_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    T_f = len(trace)
    child_info = [0, 1] # first arg is sustain criterion; second argument is release criterion
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 0
    
    for t0 in range(T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
    
        true_at_t0 = False
        
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
        
        for t_test in range(t0, T_f):
            # Get child truth information
            arg0_true = t0_truth_data[0][t_test]
            arg1_true = t0_truth_data[1][t_test]
            if arg1_true or not arg0_true:
                break
            
        if arg1_true: #tau_v_1 empty
            true_at_t0 = True
            
            tau_a[0:t_test-t0+1] = np.ones(t_test-t0+1)
            tau_s[t_test-t0] = 1
            t_s = t_test
            tau_i = tau_i - tau_a
            
        elif not arg0_true: #tau_v_0 nonempty
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)            
        else:
            true_at_t0 = True
            tau_a = np.ones(T_f-t0) 
            tau_s[-1] = 1
            t_s = T_f - 1
            tau_i = tau_i - tau_a
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node

####################################
# Release (R) Module 'R'
####################################

def release_module(status_node : sn.StatusNode, t0_truth_data, T_0): 
    trace = status_node.trace
    T_f = len(trace)
    child_info = [1, 0] # Second arg is sustain criterion; first argument is release criterion
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 1
    
    for t0 in range(T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
    
        true_at_t0 = False
        
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
        
        for t_test in range(t0, T_f):
            # Get child truth information
            arg0_true = t0_truth_data[0][t_test]
            arg1_true = t0_truth_data[1][t_test]
            if arg1_true or not arg0_true:
                break
            
        if arg1_true and arg0_true: #tau_v_1 and tau_v_0 empty
            true_at_t0 = True
            tau_a[0:t_test-t0+1] = np.ones(t_test-t0+1)
            tau_s[t_test-t0] = 1
            t_s = t_test
            tau_i = tau_i - tau_a
        elif not arg0_true: #tau_v_0 nonempty
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)            
        else:
            true_at_t0 = True
            tau_a = np.ones(T_f-t0) 
            tau_s[-1] = 1
            t_s = T_f - 1
            tau_i = tau_i - tau_a
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
        
    return status_node

####################################
# Strong Release (M) Module 'M'
####################################

def strong_release_module(status_node : sn.StatusNode, t0_truth_data, T_0):
    trace = status_node.trace
    T_f = len(trace)
    child_info = [1, 0] # Second arg is sustain criterion; first argument is release criterion
    status_node.child_info = child_info
    status_node.check_sustain_at_ts = 1
    
    for t0 in range(T_0, T_f):
        
        # Instantiate timesets
        tau_a = np.zeros(T_f-t0) 
        tau_s = np.zeros(T_f-t0) 
        tau_i = np.ones(T_f-t0) 
        tau_v = np.zeros(T_f-t0) 
    
        true_at_t0 = False
        
        # Shortcuts for efficiency (?): just store t_s
        t_s = -1
        
        for t_test in range(t0, T_f):
            # Get child truth information
            arg0_true = t0_truth_data[0][t_test]
            arg1_true = t0_truth_data[1][t_test]
            if arg1_true or not arg0_true:
                break
            
        if arg1_true and arg0_true: #tau_v_1 and tau_v_0 empty
            true_at_t0 = True
            tau_a[0:t_test-t0+1] = np.ones(t_test-t0+1)
            tau_s[t_test-t0] = 1
            t_s = t_test
            tau_i = tau_i - tau_a          
        else:
            tau_i = np.zeros(T_f-t0)
            tau_v = np.ones(T_f-t0)  
        
        status_node.tau_a_list.append(tau_a)
        status_node.tau_s_list.append(tau_s)
        status_node.tau_i_list.append(tau_i)
        status_node.tau_v_list.append(tau_v)
        status_node.true_at_t0.append(true_at_t0)
        # Extra information for signature
        status_node.t_s_list.append(t_s)
    
    return status_node



def test_operator_modules():
    
    T_f = 5
    t0 = 0
    t0_truth_data = [[False,False,True,False,False]]
    # rule_node_test = sn.RuleNode([])
    # status_node = sn.StatusNode()
    
    # status_node = to_module(status_node, t0_truth_data, t0, T_f)
        
        

if __name__ == '__main__':
    test_operator_modules()