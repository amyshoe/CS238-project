import random

# This class stores all the global parameters for the simulation

class Const(object):
    
    Z_MAX = 1.0              # in km
    Z_MIN = 0.0              # in km
    BIN_SIZE_Z = 0.01           # in km
    BINS_Z = 100             # number of bins in Z direction
    
    X_MAX = 5.0              # in km
   
    T_MAX = 275.0/3600       # in seconds
    T_MIN = 0.0              # in seconds
    BIN_SIZE_T = 1.0/3600    # in seconds
        
    ALPHA = 2.86             # in degrees
    
    Y_MAX = 0.25             # in km
    Y_MIN = -0.25            # in km
    BIN_SIZE_Y = 0.005       # in km
    BINS_Y = 100             # number of bins in Y direction
    
    VY_MIN = -50.0           # in km/hr
    VY_MAX = 50.0            # in km/hr
    BIN_SIZE_VY = 1.0        # in km/hr
    BINS_VY = 100
    
    VZ_MIN = -20.0           # in km/hr
    VZ_MAX = 20.0            # in km/hr
    BIN_SIZE_VZ = 1.0        # in km/hr
    BINS_VZ = 40
    
    M = 1.0                  # in kg
    
    Y_MAX_RUNWAY = 0.04      # in km
    Y_MIN_RUNWAY = -0.04     # in km
    
    VW_SIGMA = 1.0           # in km/hr
    VW = 20.0                # in km/hr
    VW_MAX = 25.0            # in km/hr
    VW_MIN = -25.0           # in km/hr
    BIN_SIZE_VW = 1.0
    BINS_VW = 50
    
    DELTA_VZ_MAX = 35.0      # in km/hr
    DELTA_VZ_MIN = -35.0     # in km/hr
    BIN_SIZE_DELTA_VZ = 0.35 # in km/hr
    BINS_DELTA_VZ = 200
    
    DELTA_VY_MAX = 35.0      # in km/hr
    DELTA_VY_MIN = -35.0     # in km/hr
    BIN_SIZE_DELTA_VY = 0.35 # in km/hr
    BINS_DELTA_VY = 200
    
    # Set the simulation starting parameters here
    START_Y = 0.0
    START_Z = Z_MAX
    START_VY = 0.0
    START_VZ = -13.0
    START_VW = VW
    
    # This method 
    def create_initial_state(self):
        # Generate wind direction randomly
        f = -1 if random.uniform(0, 1) < 0.5 else 1
        
        return [self.START_Y, self.START_Z, self.START_VY, self.START_VZ, f * self.START_VW]
            
    
    