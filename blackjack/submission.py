import util, math, random
from collections import defaultdict
from util import ValueIteration
from util import simulate
from util import FixedRLAlgorithm
import pdb


############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return ("Start")
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return ["Stay","Quit"]
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        result = []
        if state == "End":
            return []
        if action == "Quit":
            result.append(("End",1,10))
        else:
            result.append(("Start",0.01,1000))
            result.append(("End",0.99,10))
        return result
        # END_YOUR_CODE
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 1
        # END_YOUR_CODE

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    # state ---> (totalVal, NEXTcard_number, Deck)
    # return ---> (new_state, prob,reward)
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        # Add checks for Deck running out of cards. And add checks for #cards remaining non negative
        result = []
        #print "ACTION is:", action
        #print "STATE is:", state
        ##Check if the Deck is empty:
        if state[2] == None:
            #print []
            return []

        if action == "Take":
            if state[1] != None: ##Has peeked before
                ##Check if over the threshold??
                card_num_draw = state[1]
                card_val = self.cardValues[card_num_draw]
                if state[2][card_num_draw] > 0:##Check if we have any cards left to draw from there
                    if state[0] + card_val > self.threshold:##Went above the threshold
                        new_state = (state[0] + card_val,None,None)##It was stupid to peek and then take!!
                        #print [(new_state,1,0)]
                        return [(new_state,1,0)]
                    totalVal = state[0] + card_val
                    #print "totalVal is:", totalVal
                    NEXTcard_number = None
                    New_Deck = state[2][:card_num_draw] + (state[2][card_num_draw] -1,) + state[2][card_num_draw+1:]
                    reward = 0
                    if New_Deck == (0,) * self.multiplicity:
                        New_Deck = None
                        reward = totalVal
                    new_state = (totalVal, NEXTcard_number, New_Deck)

                    result.append((new_state,1,reward))
                    #print "RESULTS IS:", result
                    #print result
                    return result ##return the only thing that can happen
                else:
                    print "CONTROL SHOULD NEVER HAVE REACHED THIS!!"
            else: ##Has not peeked before
                #print "has not peeked before"
                #print "The current Deck is:", state[2]
                #print "totalVal is:", state[0]

                for card_num in xrange(len(self.cardValues)):
                    #print "card_num is:", card_num
                    card = self.cardValues[card_num]
                    #print "card is:", card
                    #print "state is:", state
                    prob_card = float(state[2][card_num])/float(sum(state[2]))
                    #print "prob_card is:", prob_card
                    if prob_card > 0:
                        if state[0] + card > self.threshold:##Went above the threshold
                            new_state = (state[0] + card,None,None)
                            result.append((new_state,prob_card,0))
                        else:##Did not go above the threshold
                            reward = 0
                            totalVal = state[0] + card
                            NEXTcard_number = None
                            New_Deck = state[2][:card_num] + (state[2][card_num] -1,) + state[2][card_num+1:]
                            if New_Deck == (0,)*self.multiplicity:
                                New_Deck = None
                                reward = totalVal
                            new_state = (totalVal, NEXTcard_number, New_Deck)
                            #print "The NEXT STATE is :", (new_state,prob_card,0)
                            result.append((new_state,prob_card,reward))


        elif action == "Peek":
            #print "Peek"
            #print "The CURRENT state is:", state
            if state[1]!= None:##Has peeked before! That was stupid
                #print "peeked before"
                #print []
                return []
            else:
                #print "not peeked before"
                #print "cardValues is:", state[2]
                for card_num in xrange(len(self.cardValues)):

                    card = self.cardValues[card_num]
                    prob_card = float(state[2][card_num])/sum(state[2])
                    if prob_card > 0:
                        reward = -self.peekCost
                        New_Deck = state[2]#[:card_num] + (state[2][card_num] - 1,) + state[2][card_num+1:]
                        new_state = (state[0],card_num, New_Deck)
                        result.append((new_state,prob_card,reward))


        else:##action == Quit
            #print "Quit"
            #print "reward", state[0]
            reward = state[0]
            new_state = (state[0],state[1],None)
            #print "new_state", new_state
            #print ((new_state,1,reward))
            #print [(new_state,1,reward)]
            return [(new_state,1,reward)]
        #print "RESULTS IS:", result
        #print result
        return result


        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    return BlackjackMDP(cardValues = [5,5,5,40],multiplicity = 2,threshold = 20,peekCost = 1)
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
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
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
print "======Start 4b ============="
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

##Solving using Value Iteration
algos = ValueIteration()
algos.solve(smallMDP, .0001)
#print alg.V[(0,None,(3,3,3,3,3))]
#print "VALUE ITERATION STATES ARE:", algos.pi

RL_Algo = QLearningAlgorithm(smallMDP.actions,1,identityFeatureExtractor,explorationProb = 0.2)
out = simulate(smallMDP,RL_Algo,numTrials = 30000, verbose = False)
opt_pi = {}

print "\n\n"
for state in smallMDP.states:
    opt_pi[state] = max((RL_Algo.getQ(state, action), action) for action in smallMDP.actions(state))[1]
#print "Q-LEARNING OPTIMAL STATES ARE",opt_pi
#print "\n\n\n"
count = 0
tot_count =0 

##check the difference between the two states
for state in smallMDP.states:
    tot_count += 1
    if opt_pi[state] != algos.pi[state]:
        count += 1
        #print "Q-Learning suggests this:",opt_pi[state], "Value Iteration suggests this:", algos.pi[state]

print "For SMALL MDP, Value Iteration and Q-Learning differ at:",count,"# of states in their policy, out of a total #", tot_count






# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)
largeMDP.computeStates()

algos = ValueIteration()
algos.solve(largeMDP, .0001)
#print alg.V[(0,None,(3,3,3,3,3))]
#print "VALUE ITERATION STATES ARE:", algos.pi

RL_Algo = QLearningAlgorithm(largeMDP.actions,1,identityFeatureExtractor,explorationProb = 0.2)
out = simulate(largeMDP,RL_Algo,numTrials = 30000, verbose = False)
opt_pi = {}

print "\n\n"
for state in largeMDP.states:
    opt_pi[state] = max((RL_Algo.getQ(state, action), action) for action in largeMDP.actions(state))[1]
#print "Q-LEARNING OPTIMAL STATES ARE",opt_pi
#print "\n\n\n"
count = 0
tot_count = 0
##check the difference between the two states
for state in largeMDP.states:
    tot_count += 1
    if opt_pi[state] != algos.pi[state]:
        count += 1
        #print "Q-Learning suggests this:",opt_pi[state], "Value Iteration suggests this:", algos.pi[state]

print "It differs at:",count,"# of states actions, out of a total #", tot_count
print "====================END 4b=============================="


############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).
#       Example: if the deck is (3, 4, 0 , 2), then your indicator on the presence of each card is (1,1,0,1)
#       Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE (our solution is 9 lines of code, but don't worry if you deviate from this)
    result = []
    feature1_key = (("total",total),("action",action))
    feature1_val = 1
    result.append((feature1_key,feature1_val))
    if counts != None:
        feature2_key = (tuple(sum([x>0]) for x in counts),action)
        feature2_val = 1
        result.append((feature2_key,feature2_val))
        for i in xrange(len(counts)):
            feat_key = ("Second!",i,counts[i],action)
            feat_val = 1
            result.append((feat_key,feat_val))
    else:
        pass
        # feature2_key = "Empty"
        # feature2_val = 1
        # result.append((feature2_key,feature2_val))

    return result
    #feature2 = 
    # END_YOUR_CODE
############################################################
###Running Large Test case - Again
print "==================START 4c======================="
# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)
largeMDP.computeStates()

algos = ValueIteration()
algos.solve(largeMDP, .0001)
#print alg.V[(0,None,(3,3,3,3,3))]
#print "VALUE ITERATION STATES ARE:", algos.pi

RL_Algo = QLearningAlgorithm(largeMDP.actions,1,blackjackFeatureExtractor,explorationProb = 0.2)
out = simulate(largeMDP,RL_Algo,numTrials = 30000, verbose = False)
opt_pi = {}

#print "\n\n"
for state in largeMDP.states:
    opt_pi[state] = max((RL_Algo.getQ(state, action), action) for action in largeMDP.actions(state))[1]
#sprint "Q-LEARNING OPTIMAL STATES ARE",opt_pi
#print "\n\n\n"
count = 0
tot_count = 0
##check the difference between the two states
for state in largeMDP.states:
    tot_count += 1
    if opt_pi[state] != algos.pi[state]:
        count += 1
        #print "Q-Learning suggests this:",opt_pi[state], "Value Iteration suggests this:", algos.pi[state]
print "It differs at:",count,"# of states actions, out of a total #", tot_count
print "\n\n=========================END 4c ============================"

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)
algos = ValueIteration()
algos.solve(originalMDP, .0001)
fixed_RL = FixedRLAlgorithm(algos.pi)
#print alg.V[(0,None,(3,3,3,3,3))]
#print "VALUE ITERATION STATES ARE:", algos.pi
print "\n\n======================START 4d================================="
# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)

##Calling fixed_RL with newMDP
out = simulate(newThresholdMDP,fixed_RL,numTrials = 30000, verbose = False)
print "fixed_RL sum of rewards:",sum(out)
#print "OUT IS:",out
print "\n\n\n\n\n\n\n"

##Calling Q-Learning with the newMDP
RL_Algo = QLearningAlgorithm(originalMDP.actions,1,identityFeatureExtractor,explorationProb = 0.2)
#out2 = simulate(originalMDP,RL_Algo,numTrials = 30000, verbose = False)

##run during the training phase
#RL_Algo.explorationProb = 0
out2 = simulate(newThresholdMDP,RL_Algo,numTrials = 30000, verbose = False)
print "Q Learning sum of rewards:",sum(out2)
#print out2
print "\n\n=========================END 4d================================"


