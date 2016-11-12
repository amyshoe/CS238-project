# delta_vy_max = 36 km/hr
# delta_vz_max = 36 km/hr
# v_y: -50:1:50 km/hr
# v_z: -20:1:20 km/hr
# state: (y, z, v_y, v_z, v_w)
# action: (delta_vy, delta_vz)
# update: (y + delta_vy +- 0.01(v_w^2), z + delta_vz, v_y + delta_vy +- 0.01(v_w^2), v_z + delta_vz, N(v_w, sigma))
# +=- 0.01 * v_w(km/hr)^2 <-- effect on v_y

class AirplaneSimulator:

	def __init__(self,):

	def update(s, a):
		next_y = s[0] + s[2] +   