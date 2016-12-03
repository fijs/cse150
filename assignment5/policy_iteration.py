import parse as p
import sys

def policy_iteration():
    # initiailization
    actions = ["north", "east", "south", "west"]
    rewards = p.read_rewards()
    state_map = p.read_transition_prob()
    discount = 0.5
    unchanged = True

    policy = {}

    # initialization
    util = {}
    for i in range(1, 82):
        util[i] = 0
        policy[i] = "north" # random action

    while unchanged:
        util = policy_evaluation(policy, util, discount, state_map, rewards)
        unchanged = False

        for state in state_map:
            old_policy_util = get_policy_util(state_map, state, policy[state], util)
            max_policy_util = -sys.maxint
            best_action = None

            for action in actions:
                inter_policy_util = get_policy_util(state_map, state, action, util)
                if inter_policy_util > max_policy_util:
                    best_action = action
                    max_policy_util = inter_policy_util

            if max_policy_util > old_policy_util:
                policy[state] = best_action
                unchanged = True

    print policy
    return policy


def policy_evaluation(policy, curr_util, discount, state_map, rewards):
    # u(s+1) = reward(s) + discount * (sum over new s)p(s'|s policy(s))*u(s'))
    new_util = {}

    for state in curr_util:
        policy_util = 0

        p_action = policy[state]
        trans_map = state_map[state].transition_map[p_action]

        for next_s, prob in trans_map.trans_prob.iteritems():
            policy_util += prob * curr_util[next_s]

        new_util[state] = rewards[state] + discount*policy_util

    return new_util


def get_policy_util(state_map, state, action, util):
    policy_util = 0

    trans_map = state_map[state].transition_map[action]

    for next_s, prob in trans_map.trans_prob.iteritems():
        policy_util += prob * util[next_s]

    return policy_util


if __name__ == "__main__":
    policy_iteration()
