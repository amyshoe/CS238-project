from const import Const
import numpy as np
import math, time, collections
import simulator

##Sparse product
def sparseProduct(phi,w):
    '''
    Take two sparse representations and multiplies them

    @params: 
    phi: list of (key,value pairs)
    w : weights collection.defaultdict 

    Note, phi is much smaller ~ O(5) and is represented as a list
    '''
    out = 0.0
    for (key,val) in phi:
        out += val * w[key]
    return out 

##extracting particular features
def featureExtractor(state,action):
    """
    Takes in (state,action) 
    Returns a list of (key,value) pairs
    """
    return [((state,action),1)]


##Exploratory strategy
def epsilon_greedy(action,possible_actions,num_iter):
    """
    Defines an exploratory strategy

    @params:
    actions: the best action
    possible_actions : the list of all possible actions that can be done at that point
    num_iter: the number of iterations done, to reduce the exploration accordinly

    Returns an action based upon the exploratory strategy
    """
    eps = 1/num_iter
    if eps > np.random.uniform(0,1):
        return np.random.choice(possible_actions)
    else:
        return action

##Initialize the simulator

#List of possible actions??
# We might have the get possible actions from the simulator itself. Might make sense,
# because there are some states from which we might have only certain allowed actions
Actions = [] 
W = collections.defaultdict(float)
##currently does not run anything
maxIters = 0
for num_iter in xrange(1,maxIters):
    sim = simulator.AirplaneSimulator()
    startTime = time.time()
    print "Iteration #", num_iter

    ##Learning Rate more intelligently
    step_size = 1.0/(num_iter+1)
    state = sim.get_discrete_state(sim.state)
    while not sim.end_state_flag:
        #state = sim.get_state()
        possible_actions = sim.get_action_list()
        best_action = None
        best_val = None

        for action in possible_actions:
            phis = featureExtractor(state,action)
            val = sparseProduct(phis,W)
            if val > best_val:
                best_val = val
                best_action = action
        final_action = epsilon_greedy(action, possible_actions, num_iter)

        ##the features of the old state
        old_phis = featureExtractor(state,final_action)

        ##the Q(s,a) value at the state
        val = sparseProduct(old_phis,W)

        ##Get the new_state, and the reward assosciated with the transitioning
        (reward, new_state) = sim.controller(final_action)

        ##possible actions from the new state
        possible_actions = sim.get_action_list()
        new_best_action = None
        new_best_val = None
        new_best_phis = None

        for action in possible_actions:
            phis = featureExtractor(new_state,action)
            val = sparseProduct(phis,W)
            if val > new_best_val:
                new_best_val = val
                new_best_action = action
                new_best_phis = phis

        ##update: w(s,a) --> w(s,a) - step_size*(Q(s,a) - gamma*(r+max Q(s',a'))) * beta(s,a)
        for (key,value) in phis:
            W[key] += -step_size*(best_val  - discount*(reward + best_val)*value)

    print "It took about",(time.time() - startTime)
print "Done with Q-learning"
                