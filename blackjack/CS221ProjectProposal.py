##Writing MDP for RL against a TFT agent
import util, math, random#, submission
from collections import defaultdict
from util import ValueIteration
from util import simulate
from util import FixedRLAlgorithm
import numpy as np

print "This shit"

class PrisonersDilemmaMDP(util.MDP):
	def __init__(self, numGames,PayOffFunction):        
		self.numGames = numGames
		self.PayOffFunction = PayOffFunction 

	def startState(self):
		iterationNum = 0
		rewardRL = 0
		rewardTFT = 0
		self.numGames = np.random.randint(1000,2001) #+ self.numGames
		print "NUMBERS:" ,self.numGames
		if np.random.randn() + 1 > 0.5:
			oldAction = "Yes"
		else:
			oldAction = "No"
		stateRL = (rewardRL, oldAction)
		stateVar = (iterationNum,)#,rewardRL,rewardTFT)
		#stateTFT = (rewardTFT,)
		state = (stateRL,stateVar)
		return state

    # Return set of actions possible from |state|.
	def actions(self, state):
		return ["Yes","No"]

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
	def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
		result = []
		stateRL,stateVar = state
		#print state, action, stateVar[0]

		#action = "Yes"
		if stateVar[0] >=  self.numGames:
			return result

		PAYOUT = self.PayOffFunction(action,"Yes")#stateRL[1])
		prob = 1
		newStateRL = (PAYOUT[0],action)
		#newStateTFT = (PAYOUT[1],)
		newStateVar = (stateVar[0] + 1,)

		newState = (newStateRL,newStateVar)
		result.append((newState,prob,PAYOUT[0]))
		return result


	def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
		return 1
        # END_YOUR_CODE

class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0


    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        if newState == None:
            pass #Case when it is terminal
        else:
            V_OPT = None
            for poss_action in self.actions(newState):
                ##compute V_OPT(s,a)
                V_OPT = max(V_OPT, self.getQ(newState,poss_action))
            const = self.getStepSize()*(self.getQ(state,action) - (reward + self.discount*V_OPT))
            for f,v in self.featureExtractor(state,action):
                self.weights[f] -= const*v
        return 
        # END_YOUR_CODE
# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.
def ModifiedFeatureExtractor(state, action):
	stateRL, stateVar = state
	featureKey = (stateRL, action)
	featureValue = 1
	return [(featureKey, featureValue)]

def PayOffFunction(action1, action2):
	'''
	Takes 2 actions and returns the payouts for the two agents
	'''
	if action1 == "Yes" and action2 =="Yes": return (20,20)
	if action1 == "Yes" and action2 =="No": return (5,25)
	if action1 == "No" and action2 =="Yes": return (25,5)
	if action1 == "No" and action2 =="No": return (10,10)


numGames = 4
PrisonerMDP = PrisonersDilemmaMDP(numGames,PayOffFunction)
RL_Algo = QLearningAlgorithm(PrisonerMDP.actions,1,ModifiedFeatureExtractor,explorationProb = 0.2)
out = simulate(PrisonerMDP,RL_Algo,numTrials = 1000, verbose = False)
RL_Algo.explorationProb = 0
yesState = (("Yes",),(10,))
noState  = (("No",) ,(10,))
print "Action in yesState",RL_Algo.getAction(yesState)
print "Action in noState",RL_Algo.getAction(noState)

# for state in PrisonerMDP.states:
#     opt_pi[state] = max((RL_Algo.getQ(state, action), action) for action in PrisonerMDP.actions(state))[1]






