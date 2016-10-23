# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions 
import random, util
import sys
from game import Actions


DEBUG = False

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print "bestScore ", bestScore
        #print "legalMove ", legalMoves[chosenIndex]
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        #newGhostStates = successorGameState.getGhostStates()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()

        #Variables to keep score of the move and a constant for distance tolerance
        #to the ghost as well  as initial values for food and ghost distance
        score =  0
        foodDistance = ghostDistance = 9999

        #If moving to this state gives us a food count of zero, give it top value
        if successorGameState.getNumFood() == 0:
            return 9999

        #Get ghost positions and calculate the distance to the closest ghost
        for ghostPosition in successorGameState.getGhostPositions():
          ghostDistance = min(ghostDistance, manhattanDistance(newPos,ghostPosition))

        #Add the ghost distance to the score. States with longer distances to the 
        #ghosts should be prioritized
        #score += ghostDistance
        
        #Check that the closest ghost position is less than the tolerance
        
        #If moving to a position results in death, give it bottom value
        if ghostDistance == 0:
            return -9999

        #keeping away from ghost rewarded
        #prevents ghost from jumping onto pacman
        if ghostDistance > 1:
            score += 10
        
         
        #If moving to this position results in eating food, increase score
        if successorGameState.getNumFood() < currentGameState.getNumFood():
            score += 100
        
        #Find the closest food dot available
        for foodPosition in newFood.asList():
          foodDistance = min(foodDistance, manhattanDistance(newPos,foodPosition))

        #Add the inverse of the min distance to food to the score. The smaller the distance,
        #the greater the score.
        score += 1./foodDistance

        return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        max = -sys.maxint - 1
        best_action = None
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            res_score = self.value(successor, 1, 1)
            debug("action: {}, res_score: {}".format(action, res_score))
            if res_score > max:
                max = res_score
                best_action = action

        return best_action

    def max_value(self, gameState, agentIndex, depth):
        max_val = (-sys.maxint) - 1
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            max_val = max(max_val, self.value(successor, agentIndex+1, depth))
            debug("max_val: action: {}, max_val: {}".format(action, max_val))
        return max_val

    def min_value(self, gameState, agentIndex, depth):
        min_val = sys.maxint
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            min_val = min(min_val, self.value(successor, agentIndex+1, depth))
            debug("min_value: action: {}, min_val: {}".format(action, min_val))
        return min_val

    def value(self, gameState, agentIndex, depth):
        totalAgent = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        # debug functions
        debug("value function")
        debug("agentindex is: {}, depth is: {}, self.depth is: {}".format(
            agentIndex, depth, self.depth
        ))

        if agentIndex == totalAgent:
            if depth == self.depth:
                debug("max depth, util: {}".format(self.evaluationFunction(gameState)))
                return self.evaluationFunction(gameState)
            else:
                depth += 1
                agentIndex = 0

        if agentIndex > 0:
            return self.min_value(gameState, agentIndex, depth)
        else:
            return self.max_value(gameState, agentIndex, depth)

def debug(string):
    if DEBUG:
        print string


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha_max = -sys.maxint - 1
        beta_min = sys.maxint
        best_action = None
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            res_score = self.value(successor, 1, 1, alpha_max, beta_min)
            debug("action: {}, res_score: {}".format(action, res_score))
            if res_score > alpha_max:
                alpha_max = res_score
                best_action = action

        return best_action

    def max_value(self, gameState, agentIndex, depth, alpha, beta):
        max_val = -sys.maxint - 1
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            max_val = max(max_val, self.value(successor, agentIndex+1, depth, alpha, beta))
            if max_val > beta:
                return max_val
            alpha = max(max_val, alpha)
        return max_val

    def min_value(self, gameState, agentIndex, depth, alpha, beta):
        min_val = sys.maxint
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            min_val = min(min_val, self.value(successor, agentIndex+1, depth, alpha, beta))
            if min_val < alpha:
                return min_val
            beta = min(min_val, beta)
        return min_val

    def value(self, gameState, agentIndex, depth, alpha, beta):
        totalAgent = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        # debug functions
        debug("value function")
        debug("agentindex is: {}, depth is: {}, self.depth is: {}".format(
            agentIndex, depth, self.depth
        ))

        if agentIndex == totalAgent:
            if depth == self.depth:
                debug("max depth, util: {}".format(self.evaluationFunction(gameState)))
                return self.evaluationFunction(gameState)
            else:
                depth += 1
                agentIndex = 0

        if agentIndex > 0:
            return self.min_value(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.max_value(gameState, agentIndex, depth, alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        #getAction with random for tiebreaker        
        legalMoves = gameState.getLegalActions(0)
        scores = [self.value(gameState.generateSuccessor(0, action), 1, 1) for action
            in legalMoves]
        #print "Scores : ", scores
        #for action in legalMoves:
        #    print "action : ", action
        
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        #print "action : {}, score : {}".format(legalMoves[chosenIndex],
        #    bestScore)
        
        return legalMoves[chosenIndex]
        
    def max_value(self, gameState, agentIndex, depth):
        max_val = (-sys.maxint) - 1
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            max_val = max(max_val, self.value(successor, agentIndex+1, depth))
            debug("max_val: action: {}, max_val: {}".format(action, max_val))
        return max_val

    def min_value(self, gameState, agentIndex, depth):
        min_val_sum = 0
        avg_denom = 0 
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            min_val = self.value(successor, agentIndex+1, depth)
            min_val_sum += min_val
            avg_denom += 1
            debug("min_value: action: {}, min_val: {}".format(action, min_val))
            debug("avg_denom: {} ".format(avg_denom))
        return (min_val_sum / (avg_denom * 1.0))

    def value(self, gameState, agentIndex, depth):
        totalAgent = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # debug functions
        debug("value function")
        debug("agentindex is: {}, depth is: {}, self.depth is: {}".format(
            agentIndex, depth, self.depth
        ))

        if agentIndex == totalAgent:
            if depth == self.depth:
                debug("max depth, util: {}".format(self.evaluationFunction(gameState)))
                return self.evaluationFunction(gameState)
            else:
                depth += 1
                agentIndex = 0

        if agentIndex > 0:
            return self.min_value(gameState, agentIndex, depth)
        else:
            return self.max_value(gameState, agentIndex, depth)
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Using the evaluation function from reflex agent as the base.
      Added the use of mazeDistance since accounting for walls is better
      otherwise pacman thinks food is close when it is actually far because of
      walls. Reward eating food highly, and because of reciprocal need to give 
      huge scalar weight. Also reward moving closer to food, and if ghosts are
      scared our pacman can eat him if convienent for the big points.
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

    #Variables to keep score of the move and a constant for distance tolerance
    #to the ghost as well  as initial values for food and ghost distance
    score =  0
    foodDistance = ghostDistance = 9999

    #If moving to this state gives us a food count of zero, give it top value
    if currentGameState.getNumFood() == 0:
        return sys.maxint

    #Get ghost positions and calculate the distance to the closest ghost
    #use manhattan first to find closest, then maze distance
    #otherwise if just use maze distance, computation time is too long
    for ghostPosition in currentGameState.getGhostPositions():
       ghostDistance = min(ghostDistance,
           manhattanDistance(newPos,ghostPosition))
       closestGhost = ghostPosition
    
    closestGhostMazeDist = mazeDistance(newPos, closestGhost, currentGameState) 
      
    #If moving to this position results in eating food, increase score
    #heighest weight for eating food
    score += (1./currentGameState.getNumFood()) * 1000

    
    newScaredTimes = 0
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [newScaredTimes + ghostState.scaredTimer for ghostState in newGhostStates]
    
    # ghost times accounted for if more than 1 ghost, old ghost time bad because
    # for 2 or more ghosts some ghosts can be scared but if a ghost respawns
    # pacman wouldn't have been scared of him. 
    """
    ScaredGhostsTime = []
    newGhostStates = currentGameState.getGhostStates() 
    for ghostState in newGhostStates:
        ScaredGhostsTime.append(ghostState.scaredTimer)
    """

    #Find the closest food dot available
    for foodPosition in newFood.asList():
      foodDistance = min(foodDistance,
          manhattanDistance(newPos,foodPosition))
      closestFood = foodPosition
    
    closestFoodMazeDist = mazeDistance(newPos, closestFood, currentGameState)
    #Add the inverse of the min distance to food to the score. The smaller the distance,
    #the greater the score.
    score += (1./closestFoodMazeDist)
    
    #print newScaredTimes
    #print ScaredGhostsTime
    if newScaredTimes[0] > 0:
    #if all(time > 0 for time in ScaredGhostsTime):
        score += (1./closestFoodMazeDist)
        #need to weight this alot so that it beats out closest food score
        score += (1./currentGameState.getNumFood()) * 10000
        if closestGhostMazeDist < 1:
            score += 10
        #if you can eat the ghost, worth it to eat    
        if closestGhostMazeDist == 0:
            score += 100000
    else:
        if closestGhostMazeDist > 1:
            score += 10
        if closestGhostMazeDist == 0:
            return -sys.maxint - 1
    
    return score



def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    
    x2 = int(x2)
    y2 = int(y2)
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(int(point2))
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(bfs(prob))

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()
  
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    start = problem.getStartState() 
    queue, visited = util.Queue(), []

    queue.push( (start, []) )
    visited.append(start)

    while not queue.isEmpty():
        poping = queue.pop()
        vertex, path = poping[0], poping[1]
        #print "vertex : ", vertex
        #print "path : ", path

        if problem.isGoalState(vertex):
            #print "Found solution!"
            break

        for node in problem.getSuccessors(vertex):
            state, action = node[0], node[1]
            subPath = list(path)

            if state not in visited:
                visited.append(state)
                subPath.append(action)
                queue.push( (state, subPath) )

    #print "Path is : ", path

    return path

class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost


# Abbreviation
better = betterEvaluationFunction
bfs = breadthFirstSearch

