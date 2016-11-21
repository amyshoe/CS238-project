from const import Const
import math, random

# TODO:  decide if we want the log to look nice (i.e., decide on #sigfig convention)
#        right now it's just full possible precision.

class AirplaneSimulator:
    '''
    This is the airplane simulator class
    '''
    def __init__(self):
        '''
        This is the constructor function.
        The initial state is initialized
        The minimum / maximum values for actions and state variables are stored.
        '''
        self.min_action = [Const.DELTA_VY_MIN, Const.DELTA_VZ_MIN]
        self.max_action = [Const.DELTA_VY_MAX, Const.DELTA_VZ_MAX]
        self.min_state = [Const.T_MIN, Const.Y_MIN, Const.Z_MIN, Const.VY_MIN, \
                          Const.VZ_MIN, Const.VW_MIN]
        self.max_state = [Const.T_MAX, Const.Y_MAX, Const.Z_MAX, Const.VY_MAX, \
                          Const.VZ_MAX, Const.VW_MAX]
        
        self.state = self.create_initial_state()

        with open('states_visited.txt', 'w+') as f:
            output_data = [str(value) for value in self.state]
            f.write('\t'.join(output_data) + '\n')
    
    def create_initial_state(self):
        '''
        Method to initialize the starting state
        '''
        self.time_remaining = Const.T_MAX
        
        # Generate wind directions randomly
        f = -1 if random.uniform(0, 1) < 0.5 else 1
        return [Const.START_T , Const.START_Y, Const.START_Z, \
                Const.START_VY, Const.START_VZ, f * Const.START_VW]
    
    def state_values(self):
        '''
        Method to improve readability. Returns elements in self.state (for naming conventions)
        '''
        return self.state[0], self.state[1], self.state[2], self.state[3], self.state[4], self.state[5]

    
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
        range [l_bound, r_boundset] and clips value to within that range if needed.
        
        Assumes that all inputs are 1D lists of same length
        '''
        for i, value in enumerate(values):
            if (value > r_bounds[i]):
                values[i] = r_bounds[i]
            elif (value < l_bounds[i]):
                values[i] = l_bounds[i]

    
    def update_state(self, action):
        '''
        Updates state according to a given action
        '''
        # Check if actions are within the bounds, and if not, snap it to bounds
        self.snap_to_bounds(action, self.min_action, self.max_action)

        # Name elements in state variables for readability
        t, y, z, v_y, v_z, v_w = self.state_values()
        
        # Name elements in action variable for readability
        delta_vy, delta_vz = action[0], action[1]

        # update state elements
        next_y = y + v_y * Const.BIN_SIZE_T
        next_z = z + v_z * Const.BIN_SIZE_T
        wind_effect = 0.01 * (v_w**2) * v_w/abs(v_w)
        next_vy = v_y + (delta_vy + wind_effect) * Const.BIN_SIZE_T
        next_vz = v_z + delta_vz * Const.BIN_SIZE_T
        next_vw = random.normalvariate(v_w, Const.VW_SIGMA)

        # update state, bound if needed, then record to log file
        self.state = [next_t, next_y, next_z, next_vy, next_vz, next_vw]
        self.snap_to_bounds(self.state, self.min_state, self.max_state)
        self.record_state()

        self.time_remaining -= Const.BIN_SIZE_T

