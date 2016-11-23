from const import Const
import math, random

# TODO:  decide if we want the log to look nice (i.e., decide on #sigfig convention)
# Amy needs to work on the method record_state
# Amy write nice comments for the code

class AirplaneSimulator:
    '''
    This is the airplane simulator class
    '''
    def __init__(self):
        '''
        This is the constructor function.
        The bounds, bin size and number of bins parameters are initialized for state and action.
        The initial continuous state, discrete state and penalty calculator are initialized.
        The file to write the log is also opened
        '''
        
        self.bin_sizes_states = self.get_state_bin_sizes()
        self.bin_sizes_actions = self.get_action_bin_sizes()
        
        self.min_bounds_states, self.max_bounds_states = self.get_state_bounds()
        self.min_bounds_actions, self.max_bounds_actions = self.get_action_bounds()
        
        self.total_bins_states = self.get_state_total_bins()
        self.total_bins_actions = self.get_action_total_bins()
        
        self.state = self.create_initial_state()
        self.discrete_state = self.get_discrete_state(self.state)

        with open('states_visited.txt', 'w+') as f:
            output_data = [str(value) for value in self.state]
            f.write('\t'.join(output_data) + '\n')
    
    def create_initial_state(self):
        '''
        Method to initialize the starting state
        '''        
        # Generate wind directions randomly
        f = -1 if random.uniform(0, 1) < 0.5 else 1
        return [Const.START_T , Const.START_Y, Const.START_Z, \
                Const.START_VY, Const.START_VZ, f * Const.START_VW]
    
    def get_state_bin_sizes(self):
        '''
        Method to get the bin sizes for the state variables
        ''' 
        return [Const.BIN_SIZE_T, Const.BIN_SIZE_Y, Const.BIN_SIZE_Z, \
                Const.BIN_SIZE_VY, Const.BIN_SIZE_VZ, Const.BIN_SIZE_VW]
        
    def get_action_bin_sizes(self):
        '''
        Method to get the bin sizes for the actions
        ''' 
        return [Const.BIN_SIZE_DELTA_VY, Const.BIN_SIZE_DELTA_VZ]
        
    def get_state_bounds(self):
        '''
        Method to get the min/max bounds for the state variables
        ''' 
        state_min_bound = [Const.T_MIN, Const.Y_MIN, Const.Z_MIN, \
                           Const.VY_MIN, Const.VZ_MIN, Const.VW_MIN]
        state_max_bound = [Const.T_MAX, Const.Y_MAX, Const.Z_MAX, \
                           Const.VY_MAX, Const.VZ_MAX, Const.VW_MAX]
        return state_min_bound, state_max_bound
        
    def get_action_bounds(self):
        '''
        Method to get the min/max bounds for the actions
        ''' 
        action_min_bound = [Const.DELTA_VY_MIN, Const.DELTA_VZ_MIN]
        action_max_bound = [Const.DELTA_VY_MAX, Const.DELTA_VZ_MAX]
        return action_min_bound, action_max_bound
        
    def get_state_total_bins(self):
        '''
        Method to get the total number of bins for the state variables
        ''' 
        return [Const.BINS_T, Const.BINS_Y, Const.BINS_Z, \
                Const.BINS_VY, Const.BINS_VZ, Const.BINS_VW]
        
    def get_action_total_bins(self):
        '''
        Method to get the total number of bins for the actions
        ''' 
        return [Const.BINS_DELTA_VY, Const.BINS_DELTA_VZ]
        
    def is_end_state(self, state):
        '''
        Method to detect if a state is an end state
        Return True if state is an end state, else return False
        '''
        # Name elements in state variables for readability
        t, y, z, v_y, v_z, v_w = state
        
        # Check if t <= T_MIN
        if t <= Const.T_MIN: return True
        # Check if z <= Z_MIN
        if z <= Const.Z_MIN: return True
        # Check if y <= Y_MIN or y >= Y_MAX
        if y <= Const.Y_MIN or y >= Const.Y_MAX: return True
        # If none of the above checks is true, end state is not reached
        return False
        
    def get_discrete_state(self, state):
        ''' 
        Method to return discrete state corresponding to state
        '''
        # Evaluate discrete state
        discrete_state = [int(math.floor((state_var - self.min_bounds_states[i]) \
                         / self.bin_sizes_states[i])) for i, state_var in enumerate(state)]
        
        # Check if any state index < 0, if yes, set to 0
        for i, state_var in enumerate(discrete_state):
            if state_var < 0: discrete_state[i] = 0
            
        # Check if any state index >= total bins for the state, set to total bins - 1
        for i, state_var in enumerate(discrete_state):
            max_bin = self.total_bins_states[i]
            if state_var >= max_bin: discrete_state[i] = max_bin - 1
        
        return discrete_state
        
    def get_continuous_state(self, discrete_state):
        ''' 
        Method to return continuous state corresponding to a discrete state
        Assume that discrete_state is a valid discrete state
        '''
        state = []
        state.append(float(discrete_state[0]))
        for i in range(1, len(discrete_state)):
            state.append((discrete_state[i] + 0.5) * self.bin_sizes_states[i] \
                         + self.min_bounds_states[i])        
        return state

    def update_state(self, action):
        '''
        Method to update the current simulator state according to a given action
        '''
        # Only carry out update if self.state is not an end state
        if self.is_end_state(self.state) == False:
            
            # Name elements in state variables for readability
            t, y, z, v_y, v_z, v_w = self.state
            
            # Name elements in action variable for readability
            delta_vy, delta_vz = action[0], action[1]
            
            # Update state variables
            next_t = t - Const.BIN_SIZE_T
            next_y = y + v_y * Const.BIN_SIZE_T / 3600.0
            next_z = z + v_z * Const.BIN_SIZE_T / 3600.0
            wind_effect = 0.01 * (v_w**2) * self.sign_real(v_w)
            next_vy = v_y + (delta_vy + wind_effect) * Const.BIN_SIZE_T
            next_vz = v_z + delta_vz * Const.BIN_SIZE_T
            next_vw = random.normalvariate(v_w, Const.VW_SIGMA)
            
            # Bound state variables for y and z positions, v_w
            self.snap_to_bounds(next_y, Const.Y_MIN, Const.Y_MAX)
            self.snap_to_bounds(next_z, Const.Z_MIN, float('inf'))
            self.snap_to_bounds(next_vw, Const.VW_MIN, Const.VW_MAX)
            
            # Update state
            self.state = [next_t, next_y, next_z, next_vy, next_vz, next_vw]
            self.discrete_state = self.get_discrete_state(self.state)
            
            # Record to log file
            self.record_state()
            
    def record_state(self):
        '''
        Method to keeps a log of the states (continuous) visited in simulation
        '''
        with open('states_visited.txt', 'a+') as f:
            output_data = [str(value) for value in self.state]
            f.write('\t'.join(output_data) + '\n')      

    
    def snap_to_bounds(self, value, bound_min, bound_max):
        '''
        Method to check value, bound_min, bound_max to see if value is in the 
        range [bound_min bound_max] and clips value to within that range if needed.
        '''
        if value > bound_max:
            value = bound_max
            return bound_max
        elif value < bound_min:
            value = bound_min
            return bound_min

    def sign_real(self, number):
        '''
        Method that takes a real number and returns its sign:
        return 1,  if number > 0; return -1, if number < 0; return 0, if number = 0
        '''
        if number == 0.0: return 0
        elif number > 0.0: return 1
        else: return -1
        
    def get_reward(self, state, action, next_state):
        '''
        Method that takes as input state(s), action(a), next_state(s')
        Returns the reward for (s,a,s')
        '''
        def penalty_end_state():
            