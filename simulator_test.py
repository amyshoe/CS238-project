import simulator
import matplotlib.pyplot as plt

### TODO: write a for loop with list of actions to see trends in plane behavior
sim = simulator.AirplaneSimulator()
print "Simulator state (continuous) : ", sim.state
print "Simulator state (discrete) : ", sim.discrete_state

for t in range(10):
	action = [40, 75]
	state, reward = sim.controller(action)
# print "Simulator state (continuous) : ", sim.state
# print "Simulator state (discrete) : ", sim.discrete_state
# print "Simulator state (discrete) : ", state
# print "Reward : ", reward

# action = [50, 150]
# state, reward = sim.controller(action)
# print "Simulator state (continuous) : ", sim.state
# print "Simulator state (discrete) : ", sim.discrete_state
# print "Simulator state (discrete) : ", state
# print "Reward : ", reward

# action = [40, 120]
# state, reward = sim.controller(action)
# print "Simulator state (continuous) : ", sim.state
# print "Simulator state (discrete) : ", sim.discrete_state
# print "Simulator state (discrete) : ", state
# print "Reward : ", reward

# action = [30, 100]
# state, reward = sim.controller(action)
# print "Simulator state (continuous) : ", sim.state
# print "Simulator state (discrete) : ", sim.discrete_state
# print "Simulator state (discrete) : ", state
# print "Reward : ", reward

sim.create_xy_animation(10)
# sim.create_xz_animation(10)