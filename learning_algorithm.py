from const import Const
import numpy as np
import math, time, collections
import simulator, pickle

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
    #print "The dict is:", w
    #print "The vector phi is:", phi
    for (key,val) in phi:
        out += val * w[key]
    return out 

##extracting particular features
def featureExtractor(state,action):
    """
    Takes in (state,action) 
    Returns a list of (key,value) pairs
    """
    features = []
    ## Identity features over each of the state
    #print "action passed is ",action    
    dv_y, dv_z = action[0]/5,action[1]/5
    idx = 0
    for key in state:
        #print key
        new_key = (idx,key,"Vel",dv_y)
        new_key2 = (idx,key,"Vel2",dv_z)
        if idx == 1: ##y key
            new_key = (idx,int(key/4),"Vel",dv_y)
        features.append((new_key,1))
        features.append((new_key2,1))
        idx += 1
    #t, y, z, v_y, v_z, v_w = state

    #Interaction terms for (Vy,t,)
    return features

    #return [((tuple(state),tuple(action)),1)]

def linear_approximation(Q,state,action):
    """
    Does Linear Approximation for the given state and action
    Returns the Q-value
    """
    ##Get some form of estimate for some number of positions next to it
    ## NOT BEING USED YET
    return 0


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
    eps = 0.1/num_iter
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
##currently does not run anything
maxIters = 20
discount = 0.95
minTime = 1000
file_name = "random.txt" ##File to read and write weights to and from
restart_FLAG = True
if restart_FLAG == True:
    W = collections.defaultdict(float)
else:
    print "Reading weights from the file"
    with open(file_name, 'rb') as handle:
        b = pickle.loads(handle.read())
for num_iter in xrange(1,maxIters):
    print "Iteration #", num_iter
    sim = simulator.AirplaneSimulator()
    startTime = time.time()
    #print "Iteration #", num_iter

    ##Learning Rate more intelligently
    step_size = 0.1
    state = sim.get_discrete_state(sim.state)
    while not sim.end_state_flag:
        #state = sim.get_state()
        print "state is:", state
        possible_actions = sim.get_action_list()
        best_action = None
        best_val = None
        #print "the length of possible_actions:", len(possible_actions)

        #print "The state is:", state
        ##compute the best possible action
        for action in possible_actions:
            # print "Considering :", action
            phis = featureExtractor(state,action)
            val = sparseProduct(phis,W)
            #print "\t\tVAL:", val
            if val > best_val:
                best_val = val
                print "BEST VAL", best_val
                best_action = action
        print "Best action is: ", best_action
        final_action = epsilon_greedy(best_action, possible_actions, num_iter)
        print "Chosen action is: ", final_action
        #print "Midway in the code!"
        ##the features of the old state
        print "The action it takes is:", final_action
        print "The continuous version of action:", sim.get_continuous_action(final_action)
        old_phis = featureExtractor(state,final_action)

        ##the Q(s,a) value at the state - stored as old_val
        val = sparseProduct(old_phis,W)
        old_val = val

        ##Get the new_state, and the reward assosciated with the transitioning
        (new_state, reward) = sim.controller(final_action)
        #print "the new state is:", new_state
        print "the reward is:", reward

        ##possible actions from the new state
        possible_actions = sim.get_action_list()
        if possible_actions == None:
            print "breaking because it reached an end state"
            break

        #print "the length of NEW possible_actions:", len(possible_actions)


        new_best_action = None
        new_best_val = None ##Gonna store Q(s',a')
        new_best_phis = None

        ##Compute max Q(s',a')
        for action in possible_actions:
            #print "\n\n\n\nnew state", new_state
            #print "\n\n\n\naction :", action
            phis = featureExtractor(new_state,action)
            val = sparseProduct(phis,W)
            if val > new_best_val:
                new_best_val = val ##Gonna store Q(s',a')
                new_best_action = action
                new_best_phis = phis
        ## Note its  (s,a,r,s',max a) update
        ##update: w(s,a) --> w(s,a) - step_size*(Q(s,a) - gamma*(r+max Q(s',a'))) * beta(s,a)
        for (key,value) in phis:
            W[key] += -step_size*(old_val  - discount*(reward + new_best_val)*value) 

        ##Update the current state info
        state = new_state
    final_state_analysis = sim.plane_state_analysis(sim.state)
    if sim.state[0] < minTime:
        minTime = sim.state[0]

    if final_state_analysis[2] == True:
        print "Landed safely"
    elif final_state_analysis[0] == True:
        print "Crashed"
    elif final_state_analysis[1] == True:
        print "Outside radar"
    elif final_state_analysis[3] == True:
        print "missed the landing!!"
    else:
        print "WTF!!!!!!!!!!!!!!!!"
    print sim.state


    print "Writing the weights to file!"
    with open(file_name, 'wb') as handle:
        pickle.dump(W, handle)





    print "It took about",(time.time() - startTime)
print "Done with Q-learning"
print "The Q weights states are:", W
print "The longest it has stayed is:", minTime
                