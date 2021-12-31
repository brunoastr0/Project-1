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

import math
from typing import Counter
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
    from game import actions
    s = actions.SOUTH
    w = actions.WEST
    return [s, s, s, s, w, w, s, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    frontier = util.Stack()
    explored = []
    frontierTuple = (problem.getStartState(), [])
    frontier.push(frontierTuple)

    while not frontier.isEmpty():
        currCell, actions = frontier.pop()
        if currCell not in explored:
            explored.append(currCell)
        if problem.isGoalState(currCell):
            return actions
        for childCell, direction, cost in problem.getSuccessors(currCell):
            if childCell not in explored:
                frontier.push((childCell, actions + [direction]))
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    start_node = problem.getStartState()
    visited = list()
    visited.append(start_node)
    frontierTuple = (start_node, [])
    frontier.push(frontierTuple)
    while not frontier.isEmpty():
        curr_cell, actions = frontier.pop()
        if problem.isGoalState(curr_cell):
            return actions

        for childCell, direction, cost in problem.getSuccessors(curr_cell):
            if childCell not in visited:
                visited.append(childCell)
                new_actions = actions+[direction]
                frontier.push((childCell, new_actions))

            # print(visited)
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    visited = list()
    start = problem.getStartState()
    gScore = dict()
    gScore[start] = 0.0
    frontierTuple = (start, [], gScore[start])
    frontier.push(frontierTuple, gScore[start])
    visited.append((start, gScore[start]))
    while not frontier.isEmpty():
        currCell, actions, gScore[currCell] = frontier.pop()
        if problem.isGoalState(currCell):
            return actions
        for childCell, direction, new_cost in problem.getSuccessors(currCell):
            visitedExist = False
            new_cost = new_cost + gScore[currCell]
            if childCell not in visited:
                for(visitedState, visitedCost) in visited:
                    if childCell == visitedState and new_cost >= visitedCost:
                        visitedExist = True
                if not visitedExist:
                    visited.append((childCell, new_cost))
                    frontier.push(
                        (childCell, actions+[direction], new_cost), new_cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    start_node = problem.getStartState()
    start_heuristic = heuristic(start_node, problem)
    visited_nodes = []
    frontier.push((start_node, [], 0), start_heuristic)

    while not frontier.isEmpty():
        curr_cell, actions, get_cost = frontier.pop()

        if problem.isGoalState(curr_cell):
            return actions

        if not curr_cell in visited_nodes:
            visited_nodes.append(curr_cell)
            for child_cell, direction, successor_cost in problem.getSuccessors(curr_cell):
                if not child_cell in visited_nodes:
                    new_action = actions + [direction]
                    frontier.push(
                        (child_cell, new_action, 1), problem.getCostOfActions(new_action) + heuristic(child_cell, problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
