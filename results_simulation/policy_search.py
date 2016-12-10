from const import Const
from simulator import AirplaneSimulator
import math, random, collections

"""
Perform policy search on the 1D problem
"""

def extract_features(discrete_state, sim):
    """
    Extract features for the policy search
    The policy is a linear function of the features
    """    
    # Use simulator object to get the continuous values
    state = sim.get_continuous_state([discrete_state[0], discrete_state[1], 0, \
                                      discrete_state[2], 0, discrete_state[3]])
    
    # Get the variables
    t = state[0]
    y = state[1]
    vy = state[3]
    vw = state[5]
    
    # Initialize the features vector
    features = collections.defaultdict(float)
    
    # Feature 1 : y / t
    if t > 0:
        features["y_t_ratio"] = y / t
    else:
        features["y_t_ratio"] = y / (t + Const.BIN_SIZE_T)
        
    # Feature 2 : vy
    features["vy"] = vy
    
    # Feature 3 : vw
    features["vw"] = vw
    
    # Feature 4 : constant
    features["constant"] = 1.0
    
    # Return the featuress
    return features
    
def generate_policy_action(features, weights, sim):
    """
    Take the features vector, weights vector and generate policy action
    """ 
    policy = 0.0
    for keys in features:
        policy += features[keys] * weights[keys]
    
    # Use simulator object to get the discrete action
    action = sim.get_discrete_action([policy, 0])
    
    # Return discrete action
    return action[0]
    
def rollout_evaluation(start_state, weights):
    """
    For a given weights vector, perform a single rollout
    Return the total reward
    """ 
    # Initialize the simulator from the discrete start_state
    sim = AirplaneSimulator(dim = 1, init_discrete_state = start_state)
    
    ###########################################################################
    # Perform roll out
    
    # Initialization
    total_reward = 0.0
    
    # Get initial action
    features = extract_features(start_state, sim)
    action = generate_policy_action(features, weights, sim)
    
    # Loop till end state reached
    while sim.is_end_state(sim.state) == False:
        print sim.discrete_state
        next_state, reward = sim.controller_motion_y(action)
        total_reward += reward
        
        # Generate features and action for next state
        features = extract_features(next_state, sim)
        action = generate_policy_action(features, weights, sim)
    #--------------------------------------------------------------------------
    
    # Return total_reward
    return total_reward

def initialize_weights():
    """
    This method initializes the weights vector
    Returns the weights vector
    """
    # Initialize the weights vector
    weights = collections.defaultdict(float)
    
    # Set values
    weights["y_t_ratio"] = 1.0
    weights["vy"] = 1.0
    weights["vw"] = 1.0
    weights["constant"] = 1.0
    
    # Return the weights vector
    return weights
    
def cross_entropy(weights, num_samples, num_elite_samples):
    """
    This is the cross entropy method, performs one iteration
    It takes an initial weights vector and updates the weights vector
    num_samples : rollout is performed these many times
    num_elite_samples : number of highest rating samples, MLE fit is done using these
    A normal distribution is fit over each parameter independently
    """
    
    

# Initialize the simulator
t = 10
y = 50
vy = 50
vw = 20
sim = AirplaneSimulator(dim = 1, init_discrete_state = [t, y, vy, vw])

start_state = [t, y, vy, vw]
weights = extract_features(start_state, sim)
for keys in weights:
    weights[keys] = random.uniform(0,1)

r = rollout_evaluation(start_state, weights)
print "reward = ", r