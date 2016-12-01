import parse as p
import sys

def value_iteration():
    # initiailization
    actions = ["north", "east", "south", "west"]
    rewards = p.read_rewards()
    state_map = p.read_transition_prob()
    discount = 0.9
    max_util_change = -1

    util = {}
    new_util = {}
    for i in range(1, 82):
        util[i] = 0
        new_util[i] = 0

    while max_util_change != 0:
        #print "max_util_change: {}".format(max_util_change)
        #sys.stderr.write(".")
        
        max_util_change = 0
        for key, val in new_util.iteritems():
            util[key] = val

        for _, state in state_map.iteritems():
            state_name = state.name

            action_util = -sys.maxint
            for action in actions:
                curr_score = 0.
                t_map = state.transition_map[action]
                for next_s, prob in t_map.trans_prob.iteritems():
                    curr_score += prob*util[next_s]

                action_util = max(action_util, curr_score)
            #print "action_util:{}, curr_state: {}".format(action_util, state_name)

            new_util[state_name] = rewards[state_name] + discount*action_util
            util_change = abs(new_util[state.name] - util[state.name])
            if util_change > max_util_change:
                max_util_change = util_change

    return new_util

def optimal_policy(util):
    policy = {}
    actions = ["north", "east", "south", "west"]
    state_map = p.read_transition_prob()
    
    for _, state in state_map.iteritems():
        state_name = state.name

        action_util = -sys.maxint
        policy_action = None
        for action in actions:
            curr_score = 0.
            t_map = state.transition_map[action]
            for next_s, prob in t_map.trans_prob.iteritems():
                curr_score += prob*util[next_s]

            # we can ignore states with Util = 0 since its a wall
            if curr_score > action_util and curr_score > 0.:
                policy_action = action
                action_util = curr_score
                policy[state_name] = policy_action        
    
    return policy           

def pprint_policy(util, policy):
    policy_list = []
    for state, policy in policy.iteritems():
        value = util[state]

        policy_list.append((state, value, policy.upper()))
    
    for tuple in policy_list:
        print tuple
        

if __name__ == "__main__":
    #pprint(state_map)
    utils = value_iteration()
    policy = optimal_policy(utils)
    print utils
    pprint_policy(utils, policy)
