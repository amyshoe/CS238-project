from const import Const
import random

class AirplaneSimulator:
    '''
    documentation! we'll do it later
    '''
    def __init__(self):
        '''
        fill this in yo
        '''
        self.time_elapsed = 0
        self.min_action = [Const.MIN_DELTA_VY, Const.MIN_DELTA_VZ]
        self.max_action = [Const.MAX_DELTA_VY, Const.MAX_DELTA_VZ]
        self.min_state = [Const.MIN_Y, Const.MIN_Z, Const.MIN_VY, Const.MIN_VZ, Const.MIN_VW]
        self.max_state = [Const.MAX_Y, Const.MAX_Z, Const.MAX_VY, Const.MAX_VZ, Const.MAX_VW]

        self.state = Const.START_STATE

        self.record_state()

    def get_state(self):
        ''' 
        Returns current state after discretizing
        '''
        bin_sizes = [Const.BIN_SIZE_Y, Const.BIN_SIZE_Z, Const.BIN_SIZE_VY, Const.BIN_SIZE_VZ, Const.BIN_SIZE_VW]
        discrete_state = [ceil((self.state[i] - self.min_state[i])/bin_sizes[i]) for i in range(len(self.state))]
        return discrete_state

    def record_state(self):
        '''
        Keeps a log of the states (continuous) visited in simulation
        '''
        with open('states_visited.txt', 'a+') as f:
            f.write(self.state)

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
        snap_to_bounds(action, self.min_action, self.max_action)

        y = self.state[0] + (action[0] + 0.01 * (self.state[4]**2)) * Const.BIN_SIZE_T
        z = self.state[1] + action[1] * Const.BIN_SIZE_T
        v_y = self.state[2] + (action[0] + 0.01 * (self.state[4]**2)) * Const.BIN_SIZE_T
        v_z = self.state[3] + action[1] * Const.BIN_SIZE_T
        v_w = random.randn(self.state[4], Const.SIGMA)
        
        self.state = (y, z, v_y, v_z, v_w)
        # Bound state
        snap_to_bounds(state, self.min_state, self.max_state)

        self.time_elapsed += Const.BIN_SIZE_T

        self.record_state()
