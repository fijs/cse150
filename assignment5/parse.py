# structure later
class State(object):
    transition_map = None
    name = None

    def __init__(self, name):
        self.transition_map = {}
        self.name = name

    def __getitem__(self, key):
        return self.transition_map[key]

class TransitionProb(object):
    """
    contains a map that given a next state, provides a prob
    """
    trans_prob = None
    direction = ""

    def __init__(self, direction):
        self.trans_prob = {}
        self.direction = direction

def pprint(state_map):
    for _, state in state_map.iteritems():
        tp_map = state.transition_map
        for action in tp_map:
            tp_prob_obj = state[action]
            tp_prob_map = tp_prob_obj.trans_prob

            for next_s, prob in tp_prob_map.iteritems():
                print "Curr state: {state}, direction: {dir}, next state: {next_s}, prob: {prob}".format(
                    state=state.name, dir=action, next_s=next_s, prob=prob
                )

def read_transition_prob():
    direction = ["north", "east", "south", "west"]
    state_map = {}

    for dir in direction:
        file_name = "prob_" + dir + ".txt"
        input_file = open(file_name)

        for line in input_file:
            (curr_s, next_s, prob) = line.split()
            #print "curr_s: {}, next_s: {}, prob: {}".format(curr_s, next_s, prob)

            if curr_s not in state_map:
                state_map[curr_s] = State(curr_s)

            tp_map = state_map[curr_s].transition_map
            if dir not in tp_map:
                tp_map[dir] = TransitionProb(dir)

            tp_map[dir].trans_prob[next_s] = prob

    return state_map

def read_rewards():
    reward = {}
    counter = 1
    file_name = "rewards.txt"
    input_file = open(file_name)
    for line in input_file:
        reward[counter] = int(line)
        counter += 1

    return reward


if __name__ == "__main__":
    state_map = read_transition_prob()
    #pprint(state_map)
    rewards = read_rewards()
    print rewards

























