def get_expl_at_t(tree_id, status_nodes_dict, t_star, depth):
    
    expl_data_dict = dict()
    
    t0 = 0
    t_test = t_star - t0 # comment
    first_node_id = str(tree_id)
    
    
    # Load status of \phi at t_star on \rho^{t_0...}
    current_node = status_nodes_dict[first_node_id]
    tau_a = current_node.tau_a_list[t0]
    tau_s = current_node.tau_s_list[t0]
    tau_i = current_node.tau_i_list[t0]
    
    # Interactive RSA algorithm to find next query
    if tau_a[t_test] == 1: # active 
        next_t0 = t_star
    elif tau_i[t_test] == 1 and sum(tau_s[0:t_test])>0: # inactive and prev. satisfied
        for t in range(0, t_test):
            if tau_s[t] == 1: # satisfied at t
                next_t0 = t + t0
                break
    elif tau_i[t_test] == 1:
        next_t0 = t_star    
    else: # violated 
        next_t0 = t0
    pass



def get_query(status_nodes_dict, t, t0):
    pass

