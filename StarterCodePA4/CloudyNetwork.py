#!/usr/bin/env python

from BayesianNetwork import *
# 
#   * Creates and tests the alarm network as given in the book.
#   
class CloudyNetwork(object):
    """ generated source for class CloudyNetwork """
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        cloudnet = BayesianNetwork()
        #  Add variables to network
        cloudy = RandomVariable("Cloudy")
        sprinkler = RandomVariable("Sprinkler")
        rain = RandomVariable("Rain")
        wetGrass = RandomVariable("wetGrass")
        cloudnet.addVariable(cloudy)
        cloudnet.addVariable(sprinkler)
        cloudnet.addVariable(rain)
        cloudnet.addVariable(wetGrass)
        #  Add edges to network
        cloudnet.addEdge(cloudy, sprinkler)
        cloudnet.addEdge(cloudy, rain)
        cloudnet.addEdge(sprinkler, wetGrass)
        cloudnet.addEdge(rain, wetGrass)
        #  Initialize probability tables
        cloudyProbs = [.5]
        sprinklerProbs = [0.1, 0.5]
        rainProbs = [0.8, 0.2]
        wetGrassProbs = [0.99, 0.9, .9, 0]
        cloudnet.setProbabilities(cloudy, cloudyProbs)
        cloudnet.setProbabilities(sprinkler, sprinklerProbs)
        cloudnet.setProbabilities(rain, rainProbs)
        cloudnet.setProbabilities(wetGrass, wetGrassProbs)

        #  Perform sampling tests
        #  ----------------------
        #  P(J=1|B=0,E=1) = TODO in writeup
        trial_list = [50, 100, 500, 1000, 5000, 10000]
        #print("Test 1")
        #given1 = {}
        #given1[rain]= True
        #given1[cloudy]=True

        #for trial in trial_list:
        #    print "Trial with number: {}".format(trial)
        #    print("rejection sampling: " +str(cloudnet.performRejectionSampling(wetGrass, given1, trial)))
        #    print("weighted sampling: " + str(cloudnet.performWeightedSampling(wetGrass, given1, trial)))
        #    print("gibbs sampling: " + str(cloudnet.performGibbsSampling(wetGrass, given1, trial)))
        #    print
        #  P(Rain=1|Sprinkler=1) = TODO in writeup
        print("Test 2")
        given2 = {}
        given2[rain]=True
        for trial in trial_list:
            print "Trial with number: {}".format(trial)
            print("weighted sampling: " + str(cloudnet.performWeightedSampling(sprinkler, given2, trial)))
            print("rejection sampling: " + str(cloudnet.performRejectionSampling(sprinkler, given2, trial)))
            print("gibbs sampling: " + str(cloudnet.performGibbsSampling(sprinkler, given2, trial)))
            print


if __name__ == '__main__':
    import sys
    CloudyNetwork.main(sys.argv)
import sys
#CloudyNetwork.main(sys.argv)
