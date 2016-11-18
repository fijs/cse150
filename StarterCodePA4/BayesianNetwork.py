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

    def print_variable(self, top_order):
        """
        testing whether top order was correct
        :param top_order: list of node in topological order
        :return: nothing
        """
        for node in top_order:
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
        curr_num_sample = 0
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

        res = (num_query_sample*1.0)/curr_num_sample
        print "number of query sample: {}".format(num_query_sample)
        print "total sample: {}".format(curr_num_sample)
        print "res: {}".format(res)

        return res

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using weighted sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of weighted samples to perform
    #     
    def performWeightedSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performWeightedSampling """
        #  TODO
        return 0

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
        return 0

