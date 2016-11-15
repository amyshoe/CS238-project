from const import Const
import math
import random

# TODO:  check update formulas in update() function --- Rahul
# TODO:  decide if we want the log to look nice (i.e., decide on #sigfig convention)
#        right now it's just full possible precision.

class AirplaneSimulator:
    '''
    documentation! we'll do it later
    '''
    def __init__(self):
        '''
        fill this in yo
        '''
        self.time_elapsed = 0
        self.min_action = [Const.DELTA_VY_MIN, Const.DELTA_VZ_MIN]
        self.max_action = [Const.DELTA_VY_MAX, Const.DELTA_VZ_MAX]
        self.min_state = [Const.Y_MIN, Const.Z_MIN, Const.VY_MIN, Const.VZ_MIN, Const.VW_MIN]
        self.max_state = [Const.Y_MAX, Const.Z_MAX, Const.VY_MAX, Const.VZ_MAX, Const.VW_MAX]

        const = Const()
        self.state = const.create_initial_state()

        with open('states_visited.txt', 'w+') as f:
            output_data = [str(value) for value in self.state]
            f.write('\t'.join(output_data) + '\n')

    
    def state_values(self):
        '''
        Method to improve readability. Returns elements in self.state (for naming conventions)
        '''
        return self.state[0], self.state[1], self.state[2], self.state[3], self.state[4]

    
    def get_state(self):
        ''' 
        Returns current state after discretizing
        '''
        print "Continuous state: ", self.state
        bin_sizes = [Const.BIN_SIZE_Y, Const.BIN_SIZE_Z, Const.BIN_SIZE_VY, Const.BIN_SIZE_VZ, Const.BIN_SIZE_VW]
        discrete_state = [math.ceil((self.state[i] - self.min_state[i])/bin_sizes[i]) for i in range(len(self.state))]
        return discrete_state

    
    def record_state(self):
        '''
        Keeps a log of the states (continuous) visited in simulation
        '''
        with open('states_visited.txt', 'a+') as f:
            output_data = [str(value) for value in self.state]
            f.write('\t'.join(output_data) + '\n')      

    
    def snap_to_bounds(self, values, l_bounds, r_bounds):
        '''
        Checks values, l_bounds, r_bounds elementwise to see if value is in the 
        range [l_bound, r_boundset] and clips value to within that range if needed
        '''
        for i, value in enumerate(values):
            if (value > r_bounds[i]):
                values[i] = r_bounds[i]
            elif (value < l_bounds[i]):
                values[i] = l_bounds[i]

    
    def update(self, action):
        '''
        Updates state according to a given action
        '''
        # Bound actions
        self.snap_to_bounds(action, self.min_action, self.max_action)

        # Name elements in state variable for readability
        y, z, v_y, v_z, v_w = self.state_values()
        # Name elements in action variable for readibility
        delta_vy, delta_vz = action[0], action[1]

        # update state elements
        next_y = y + v_y * Const.BIN_SIZE_T
        next_z = z + v_z * Const.BIN_SIZE_T
        wind_effect = 0.01 * (v_w**2) * v_w/abs(v_w)
        next_vy = v_y + (delta_vy + wind_effect) * Const.BIN_SIZE_T
        next_vz = v_z + delta_vz * Const.BIN_SIZE_T
        next_vw = random.normalvariate(v_w, Const.VW_SIGMA)

        # update state, bound if needed, then record to log file
        self.state = [next_y, next_z, next_vy, next_vz, next_vw]
        self.snap_to_bounds(self.state, self.min_state, self.max_state)
        self.record_state()

        self.time_elapsed += Const.BIN_SIZE_T

