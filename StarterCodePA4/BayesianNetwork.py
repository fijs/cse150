#!/usr/bin/env python
""" generated source for module BayesianNetwork """
from Assignment4 import *
import random
import Queue

#
#  * A bayesian network
#  * @author Panqu
#  
class BayesianNetwork(object):
    """ generated source for class BayesianNetwork """
    # 
    #     * Mapping of random variables to nodes in the network
    #     
    varMap = None

    # 
    #     * Edges in this network
    #     
    edges = None

    # 
    #     * Nodes in the network with no parents
    #     
    rootNodes = None

    # 
    #     * Default constructor initializes empty network
    #     
    def __init__(self):
        """ generated source for method __init__ """
        self.varMap = {}
        self.edges = []
        self.rootNodes = []

    # 
    #     * Add a random variable to this network
    #     * @param variable Variable to add
    #     
    def addVariable(self, variable):
        """ generated source for method addVariable """
        node = Node(variable)
        self.varMap[variable]=node
        self.rootNodes.append(node)

    # 
    #     * Add a new edge between two random variables already in this network
    #     * @param cause Parent/source node
    #     * @param effect Child/destination node
    #     
    def addEdge(self, cause, effect):
        """ generated source for method addEdge """
        source = self.varMap.get(cause)
        dest = self.varMap.get(effect)
        self.edges.append(Edge(source, dest))
        source.addChild(dest)
        dest.addParent(source)
        if dest in self.rootNodes:
            self.rootNodes.remove(dest)

    # 
    #     * Sets the CPT variable in the bayesian network (probability of
    #     * this variable given its parents)
    #     * @param variable Variable whose CPT we are setting
    #     * @param probabilities List of probabilities P(V=true|P1,P2...), that must be ordered as follows.
    #       Write out the cpt by hand, with each column representing one of the parents (in alphabetical order).
    #       Then assign these parent variables true/false based on the following order: ...tt, ...tf, ...ft, ...ff.
    #       The assignments in the right most column, P(V=true|P1,P2,...), will be the values you should pass in as probabilities here.
    #     
    def setProbabilities(self, variable, probabilities):
        """ generated source for method setProbabilities """
        probList = []
        for probability in probabilities:
            probList.append(probability)
        self.varMap.get(variable).setProbabilities(probList)


    def get_topological_order(self):
        top_order = []
        queue = Queue.Queue()

        for node in self.rootNodes:
            queue.put(node)

        while not queue.empty():
            node = queue.get()
            if node in top_order:
                top_order.remove(node)
            top_order.append(node)

            for child in node.children:
                queue.put(child)

        return top_order

    def print_variable(self, node_list):
        """
        given a node list, print var name in node
        :param node_list: list of node
        :return: nothing
        """
        for node in node_list:
            print node.variable.getName()

    #
    #     * Returns an estimate of P(queryVal=true|givenVars) using rejection sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of rejection samples to perform
    #     
    def performRejectionSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performRejectionSampling """
        #  TODO
        curr_num_sample = 1.0
        num_query_sample = 0
        top_order = self.get_topological_order()
        queryVar_name = queryVar.getName()

        while(curr_num_sample < numSamples):
            # sample each variable topologically
            # if the sampled evidence var does not match givenVars, reject
            # flip coin based on cpt, p(x|parents(x))
            assign = True
            assignment = {}
            for node in top_order:
                var_name = node.variable.getName()
                true_prob = node.getProbability(assignment, True)
                node_sample_prob = random.random()
                if node_sample_prob <= true_prob:
                    assignment[var_name] = True
                else:
                    assignment[var_name] = False

                if node.variable in givenVars:
                    if assignment[var_name] != givenVars[node.variable]:
                        assign = False
                        break

                # print "node {}".format(node.variable.getName())
                # print "true prob: {}",format(true_prob)
                # print "sample_prob: {}".format(node_sample_prob)
                # print assignment

            if assign:
                curr_num_sample += 1
                if assignment[queryVar_name]:
                    num_query_sample += 1

        res = (num_query_sample)/curr_num_sample
        print "number of query sample: {}".format(num_query_sample)
        print "total sample: {}".format(curr_num_sample)
        print "res: {}".format(res)

        return res

    #performs probability calculations for P(queryVar=true|givenVars)
    def normalizeW(self, W, queryVar):

        queryVarTrueEvents, totalEvents = 0.0, 0.0

        #print (queryVar.getName(),True)

        #iterate over event, weight pairs in W
        for x, w in W.items():

            #print x, w
            #Check if queryVar is true in event x, if so add 1 to count
            if (queryVar.getName(),True) in x: queryVarTrueEvents += w

            totalEvents += w

        #print W
        #print queryVarTrueEvents, totalEvents
        return queryVarTrueEvents/totalEvents
        #return 13

    #sample the bayes network and return an event and a weight
    def getWeigthedSample(self, givenVars):

        w, assignments = 1., {}

        for v in givenVars: assignments[v.getName()] = givenVars[v]
        #print assignments

        for var in sorted(self.varMap):

            varName = var.getName()

            rand = random.random()

            if varName in assignments:
                #get node associated with random variable, then get probability of that node
                w *= self.varMap.get(var).getProbability(assignments, assignments[varName]) 
            else:
                if rand > self.varMap.get(var).getProbability(assignments, True):
                    assignments[varName] = False
                else:
                    assignments[varName] = True

        return frozenset(assignments.items()), w

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using weighted sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of weighted samples to perform
    #     
    def performWeightedSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performWeightedSampling """
        #  TODO

        #print numSamples
        #c1, c2 = 0,0
        W = {}

        for i in range(numSamples):

            (x,w) = self.getWeigthedSample(givenVars)

            if x in W: 
                #c1 += 1
                W[x] += w
            else: 
                #c2 += 1
                W[x] = w

        #print "c1 is: ",c1," and c2 is: ",c2
        return self.normalizeW(W,queryVar)

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using Gibbs sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numTrials Number of Gibbs trials to perform, where a single trial consists of assignments to ALL
    #       non-evidence variables (ie. not a single state change, but a state change of all non-evidence variables)
    #     
    def performGibbsSampling(self, queryVar, givenVars, numTrials):
        """ generated source for method performGibbsSampling """
        #  TODO
        num_query_sample = 1.0
        total_sample = 0
        query_var_name = queryVar.getName()
        non_evidence_nodes = []
        # get all non evidence nodes
        for var in self.varMap:
            if var not in givenVars:
                # TODO: check this
                non_evidence_nodes.append(self.varMap[var])


        # randomly assign non evidence variables
        curr_assign = self.random_initialize(non_evidence_nodes)
        # fix evidence variables
        for var in givenVars:
            curr_assign[var.getName()] = givenVars[var]

        ### testing comments
        #print "non evidendce nodes:"
        #self.print_variable(non_evidence_nodes)
        #print "curr assignment: {}".format(curr_assign)

        # gibs sampling
        for i in range(0, numTrials):
            for node in non_evidence_nodes:
                var_name = node.variable.getName()

                mb_list = []
                # iterate through both values since we don't know exact,
                # but can normalize later on
                for value in [True, False]:
                    curr_assign[var_name] = value
                    curr_prob = node.getProbability(curr_assign, value)
                    for child in node.getChildren():
                        child_name = child.variable.getName()
                        curr_prob *= child.getProbability(curr_assign, curr_assign[child_name])
                    mb_list.append(curr_prob)

                mb_list = self.normalize(mb_list)

                node_sample_prob = random.random()
                node_prob = mb_list[0]

                if node_sample_prob <= node_prob:
                    curr_assign[var_name] = True
                else:
                    curr_assign[var_name] = False

                ### testing comments
                #print "current node: {}".format(var_name)
                #print "curr assign: {}".format(curr_assign)
                #print "mb list: {}".format(mb_list)
                #print "node prob: {}".format(node_prob)
                # print "curr non_evidence var: {}".format(var_name)
                # print "markov assignment: {}".format(mb_assign)
                # print "true prob: {}".format(true_prob)

                if curr_assign[query_var_name]:
                    num_query_sample += 1

                total_sample += 1

        return num_query_sample/total_sample

    def normalize(self, prob_list):
        norm_factor = reduce(lambda x, y: x+y, prob_list, 0.)

        return map(lambda x: x/norm_factor, prob_list)

    def random_initialize(self, node_list):
        """
        randomly assign values to variable in node_list
        by flipping a coin
        :param node_list: list of nodes
        :return:
        """
        rand_map = {}
        for node in node_list:
            var_name = node.variable.getName()
            node_sample_prob = random.random()
            if node_sample_prob < 0.5:
                rand_map[var_name] = True
            else:
                rand_map[var_name] = False

        return rand_map

    def markov_blanket(self, node):
        """
        markov blanket of a node
         1. parents of node
         2. descendants of node
         3. parents of descendants of node
        :param var:
        :return: list of nodes that are markov blanket of param node
        """
        mb = []
        children = node.getChildren()
        mb.extend(children)
        mb.extend(node.getParents())
        for child in children:
            mb.extend(child.getParents())

        return mb

    def get_mb_assignment(self, node_list, curr_map):
        """
        a map with var_list assigned according to a_map
        :return:
        """
        mb_map = {}
        for node in node_list:
            var_name = node.variable.getName()
            mb_map[var_name] = curr_map[var_name]

        return mb_map
