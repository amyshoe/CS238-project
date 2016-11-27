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
    #print "phi is:", phi
    #print "w is :", w
    out = 0.0

    for (key,val) in phi:
        out += val * w[tuple(key)]
    return out 

##extracting particular features
def featureExtractor(state,action):
    """
    Takes in (state,action) 
    Returns a list of (key,value) pairs
    """
    return [((tuple(state),tuple(action)),1)]


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
    #print "possible actions are:",possible_actions
    #print "action, num_iter", action,num_iter
    if eps > np.random.uniform(0,1):
        idx = np.random.randint(len(possible_actions))
        return possible_actions[idx]
    else:
        return action

##Initialize the simulator

#List of possible actions??
# We might have the get possible actions from the simulator itself. Might make sense,
# because there are some states from which we might have only certain allowed actions
Actions = [] 
W = collections.defaultdict(float)
##currently does not run anything
maxIters = 2
discount = 0.95
for num_iter in xrange(1,maxIters):
    print "Iteration #", num_iter
    sim = simulator.AirplaneSimulator()
    startTime = time.time()
    #print "Iteration #", num_iter

    ##Learning Rate more intelligently
    step_size = 1.0/(num_iter+1)
    state = sim.get_discrete_state(sim.state)
    while not sim.end_state_flag:
        #state = sim.get_state()
        print "Running at time step:!", state[0]
        possible_actions = sim.get_action_list()
        best_action = None
        best_val = None
        #print "the length of possible_actions:", len(possible_actions)

        #print "The state is:", state
        for action in possible_actions:
            #print "Considering :", action
            phis = featureExtractor(state,action)
            val = sparseProduct(phis,W)
            if val > best_val:
                best_val = val
                best_action = action
        final_action = epsilon_greedy(action, possible_actions, num_iter)
        #print "Midway in the code!"
        ##the features of the old state
        old_phis = featureExtractor(state,final_action)

        ##the Q(s,a) value at the state
        val = sparseProduct(old_phis,W)

        ##Get the new_state, and the reward assosciated with the transitioning
        (new_state, reward) = sim.controller(final_action)
        #print "the new state is:", new_state
        #print "the reward is:", reward

        ##possible actions from the new state
        possible_actions = sim.get_action_list()
        if possible_actions == None:
            print "breaking because it reached an end state"
            break

        #print "the length of NEW possible_actions:", len(possible_actions)


        new_best_action = None
        new_best_val = None
        new_best_phis = None

        for action in possible_actions:
            #print "\n\n\n\nnew state", new_state
            #print "\n\n\n\naction :", action
            phis = featureExtractor(new_state,action)
            val = sparseProduct(phis,W)
            if val > new_best_val:
                new_best_val = val
                new_best_action = action
                new_best_phis = phis

        ##update: w(s,a) --> w(s,a) - step_size*(Q(s,a) - gamma*(r+max Q(s',a'))) * beta(s,a)
        for (key,value) in phis:
            W[key] += -step_size*(best_val  - discount*(reward + best_val)*value)
        state = new_state

    print "It took about",(time.time() - startTime)
print "Done with Q-learning"
                