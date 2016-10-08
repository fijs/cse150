# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from game import Directions
import util

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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    #from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def getMove(move):

    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    #print "Move is: ", move

    if   move == s: return s
    elif move == w: return w
    elif move == e: return e
    elif move == n: return n
    else:
        util.raiseInvalidMove()


def extractMoves(path):

    moves = []

    for element in path:

        #print "Element is: ", element

        moves.append(getMove(element[1]))

    return moves


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    start = problem.getStartState() 
    stack, visited = util.Stack(), []
    
    stack.push( (start, []) )
    visited.append(start)

    while not stack.isEmpty():

        poping = stack.pop()

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
                stack.push( (state, subPath) )

    #print "Path is : ", path

    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
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

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    start = problem.getStartState() 
    queue, visited = util.PriorityQueue(), []
    
    queue.push( (start, [], 0), 0 )
    visited.append(start)

    while not queue.isEmpty():
        poping = queue.pop()
        vertex, path, cost = poping[0], poping[1], poping[2]

        #print "vertex : ", vertex
        #print "path : ", path

        if problem.isGoalState(vertex): 

            #print "Found solution!"
            break

        for node in problem.getSuccessors(vertex):
            state, action, stepCost = node[0], node[1], node[2]
            subPath = list(path)

            if state not in visited:

                totalCost = cost + stepCost
                visited.append(state)
                subPath.append(action)
                queue.push( (state, subPath, totalCost), totalCost )

    #print "Path is : ", path

    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
      
    start = problem.getStartState()
    
    queue = util.PriorityQueue()
    visited = [] 
    # ((vertex, path, cost), priority)
    queue.push( (start, [], 0), 0)
    visited.append(start)

    while not queue.isEmpty():
        popped = queue.pop()
        #print "popped is : ", popped
        vertex, path, cost = popped
        #heurCost = heuristic(vertex,problem)
        #print "V is : ", vertex
        #print "Heur is : ", heurCost

        if problem.isGoalState(vertex):
            break

        for node in problem.getSuccessors(vertex):
            state, action, stepCost = node
            subPath = list(path)

            if state not in visited:
                visited.append(state)
                subPath.append(action)
                gn_cost = cost+stepCost
                fn_cost = gn_cost+heuristic(state, problem)
                queue.push((state, subPath, gn_cost), fn_cost)

    #print "Path is : ", path
    
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
