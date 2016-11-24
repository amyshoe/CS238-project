import simulator
import matplotlib.pyplot as plt

### TODO: write a for loop with list of actions to see trends in plane behavior
sim = simulator.AirplaneSimulator()
print "Simulator state (continuous) : ", sim.state
print "Simulator state (discrete) : ", sim.discrete_state

action1 = [0.25, -30]
sim.update_state(action1)
print "Simulator state (continuous) : ", sim.state
print "Simulator state (discrete) : ", sim.discrete_state

action1 = [0.25, 3]
sim.update_state(action1)
print "Simulator state (continuous) : ", sim.state
print "Simulator state (discrete) : ", sim.discrete_state
