import simulator
import matplotlib.pyplot as plt

### TODO: write a for loop with list of actions to see trends in plane behavior
sim = simulator.AirplaneSimulator()
print "Simulator state (continuous) : ", sim.state
print "Simulator state (discrete) : ", sim.discrete_state

action1 = [40, 75]
state, reward = sim.controller(action1)
print "Simulator state (continuous) : ", sim.state
print "Simulator state (discrete) : ", sim.discrete_state
print "Simulator state (discrete) : ", state
print "Reward : ", reward

action1 = [50, 150]
state, reward = sim.controller(action1)
print "Simulator state (continuous) : ", sim.state
print "Simulator state (discrete) : ", sim.discrete_state
print "Simulator state (discrete) : ", state
print "Reward : ", reward