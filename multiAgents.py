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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Our pre-determined weights
        FOOD_WEIGHT = 0.8
        GHOST_WEIGHT = 0.5
        SCARED_WEIGHT = 0.15

        # The closest pellet to Pacman.
        closest_pellet = 1
        if newFood.asList():
            # Good lord Python's syntax is so slick :)
            closest_pellet = min(util.manhattanDistance(newPos, pellet) for pellet in newFood.asList())

        # Distance from pacman to gHoStS
        ghost_distances = 1
        for ghost in newGhostStates:
            ghost_distances += util.manhattanDistance(newPos, ghost.getPosition())

        # Amount of time left with ghosts being scared.
        scared_time = 1
        for scared in newScaredTimes:
            scared_time += scared

        # Adjusted values with weights. Negative means we want pacman to avoid states with large numbers here.
        FOOD_ADJ = (FOOD_WEIGHT / float(closest_pellet))
        GHOSTS_ADJ = (GHOST_WEIGHT / float(ghost_distances)) * -1
        SCARED_ADJ = (SCARED_WEIGHT / float(scared_time))

        return successorGameState.getScore() + FOOD_ADJ + GHOSTS_ADJ + SCARED_ADJ


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(currentGameState, agent_number, depth):
            # We've hit the bottom of the specified depth.
            if depth == self.depth or currentGameState.isLose() or currentGameState.isWin():
                return (self.evaluationFunction(currentGameState),Directions.STOP)

            # Pacman
            if agent_number == 0:
                v = float('-inf')
                move = Directions.STOP
                for possible_move in currentGameState.getLegalActions(agent_number):
                    val = minimax(currentGameState.generateSuccessor(agent_number, possible_move), 1, depth)
                    if v < val[0]:
                        v = val[0]
                        move = possible_move
                # We're pacman, so we're positive.
                return (v,move)
            # Ghosts
            else:
                # Cycling through ghosts.
                next_agent = agent_number + 1
                if next_agent == gameState.getNumAgents():
                    next_agent = 0

                # Gotta love me some ternary operators :)
                depth += 1 if next_agent == 0 else 0

                v = float('inf')
                for possible_move in currentGameState.getLegalActions(agent_number):
                    val = minimax(currentGameState.generateSuccessor(agent_number, possible_move), next_agent, depth)
                    if v > val[0]:
                        v = val[0]
                # Since the ghosts are our adversaries, they're negative, stop is ignored.
                return (v, Directions.STOP)

        # returns the best found action for pacman to take.
        return minimax(gameState, 0, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimax(currentGameState, agent_number, depth,a,b):
            # We've hit the bottom of the specified depth.
            if depth == self.depth or currentGameState.isLose() or currentGameState.isWin():
                return (self.evaluationFunction(currentGameState),Directions.STOP) #stop is a placefiller, not actually used

            # Pacman
            if agent_number == 0:
                v = float('-inf')
                move = Directions.STOP
                for possible_move in currentGameState.getLegalActions(agent_number):
                    val = minimax(currentGameState.generateSuccessor(agent_number, possible_move), 1, depth,a,b)
                    if v < val[0]:
                        v = val[0]
                        move = possible_move
                    a = max(a,v)
                    if a > b:
                        return(v,move)
                # We're pacman, so we're positive. returning the best move for pacman to choose from
                return (v,move)
            # Ghosts
            else:
                # Cycling through ghosts.
                next_agent = agent_number + 1
                if next_agent == gameState.getNumAgents():
                    next_agent = 0

                # Gotta love me some ternary operators :)
                depth += 1 if next_agent == 0 else 0

                v = float('inf')
                for possible_move in currentGameState.getLegalActions(agent_number):
                    val = minimax(currentGameState.generateSuccessor(agent_number, possible_move), next_agent, depth,a,b)
                    if v > val[0]:
                        v = val[0]
                    #used for pruning
                    b = min(b,v)
                    if a > b:
                        return (v,Directions.STOP)
                # Since the ghosts are our adversaries, they're negative, direction doesn't matter so using stop as a placefiller
                return (v, Directions.STOP)


        #gets the value and best action with pruning, so have to make a and b -infinity and infinity for min and max comparisons
        val = minimax(gameState, 0, 0,float('-inf'),float('inf'))
        return val[1]


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
        def minimax(currentGameState, agent_number, depth):
            # We've hit the bottom of the specified depth.
            if depth == self.depth or currentGameState.isLose() or currentGameState.isWin():
                return self.evaluationFunction(currentGameState)

            # Pacman
            if agent_number == 0:
                lst = []
                for possible_move in currentGameState.getLegalActions(agent_number):
                    val = minimax(currentGameState.generateSuccessor(agent_number, possible_move), 1, depth)
                    lst.append(val)

                # We're pacman, so we're positive.
                return max(lst)
            # Ghosts
            else:
                # Cycling through ghosts.
                next_agent = agent_number + 1
                if next_agent == gameState.getNumAgents():
                    next_agent = 0

                # Gotta love me some ternary operators :)
                depth += 1 if next_agent == 0 else 0

                lst = []
                sum = 0
                for possible_move in currentGameState.getLegalActions(agent_number):
                    val = minimax(currentGameState.generateSuccessor(agent_number, possible_move), next_agent, depth)
                    lst.append(val)
                    sum += val

                # Since the ghosts are our adversaries but we're not sure they're the brightest needle in the heystack, we allow room for error.
                return sum / len(lst)

        # Root node jump-start.
        utility = float('-inf')
        corresponding_move = None
        for legalMove in gameState.getLegalActions(0):
            val = minimax(gameState.generateSuccessor(0, legalMove), 1, 0)
            # We've found a more desirable move.
            if val > utility:
                utility = val
                corresponding_move = legalMove

        # Always returns corresponding_move, but wanting to make sure there's a default in case something weird happens.
        return Directions.NORTH if corresponding_move is None else corresponding_move


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
