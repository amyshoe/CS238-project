import simulator
import matplotlib.pyplot as plt

sim = simulator.AirplaneSimulator(dim = 1, init_discrete_state = [10, 50, 50, 25])
print "Simulator state (continuous) : ", sim.state
print "Simulator state (discrete) : ", sim.discrete_state

for t in range(3):
    action = 100
    state, reward = sim.controller_motion_y(action)
    print "Simulator state (continuous) : ", sim.state
    print "Simulator state (discrete) : ", state
    print "Reward : ", reward
    print "Action : ", action
    print " "