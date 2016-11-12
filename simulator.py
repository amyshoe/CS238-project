# delta_vy_max = 36 km/hr
# delta_vz_max = 36 km/hr
# v_y: -50:1:50 km/hr
# v_z: -20:1:20 km/hr
# state: (y, z, v_y, v_z, v_w)
# action: (delta_vy, delta_vz)
# update: (y + delta_vy +- 0.01(v_w^2), z + delta_vz, v_y + delta_vy +- 0.01(v_w^2), v_z + delta_vz, N(v_w, sigma))
# +=- 0.01 * v_w(km/hr)^2 <-- effect on v_y
import random

class AirplaneSimulator:
	'''
	documentation! we'll do it later
	'''
	def __init__(self, input_params):
		'''
		fill this in yo
		'''
		self.state = None
		self.sigma = 1
		self.possible_actions = None
		self.time_step = 1

		# Initialize class attributes!
		self.load_params(input_params)

	def load_params(self, input_params):
		'''
		doc string! do it later
		'''
		# set the attributes!!!!

	def update(self, action):
		'''
		Updates state according to a given action
		'''
		if not action in self.possible_actions:
			print "Action is not possible."
			return False
		y = self.state[0] + (action[0] + 0.01 * (self.state[4]**2)) * self.time_step
		z = self.state[1] + action[1] * self.time_step
		v_y = self.state[2] + (action[0] + 0.01 * (self.state[4]**2)) * self.time_step
		v_z = self.state[3] + action[1] * self.time_step
		v_w = random.randn(self.state[4], self.sigma)
		self.state = (y, z, v_y, v_z, v_w)

	def get_state(self):
		''' 
		Returns current state 
		'''
		return self.state


