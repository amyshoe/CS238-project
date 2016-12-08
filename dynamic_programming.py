from const import Const
from simulator import AirplaneSimulator
import math, random, collections
import numpy as np

"""
Dynamic programming based policy search
"""
    
def rollout_evaluation_1step(start_state, action):
    """
    Assume that start_state is always among the valid discrete states
    Take the action and return estimate of (reward + Vopt)
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