# This class stores all the global parameters for the simulation

class Const(object):
    
    # Position parameters
    Z_MAX = 1.0              # in km
    Z_MIN = 0.0              # in km
    BIN_SIZE_Z = 0.01        # in km
    BINS_Z = 100             # number of bins in Z direction
    
    X_MAX = 5.0              # in km
    
    Y_MAX = 0.25             # in km
    Y_MIN = -0.25            # in km
    BIN_SIZE_Y = 0.005       # in km
    BINS_Y = 100             # number of bins in Y direction
    
    # Time parameters
    T_MAX = 275.0            # in seconds
    T_MIN = 0.0              # in seconds
    BIN_SIZE_T = 1.0         # in seconds
    BINS_T = 276             # number of bins in T
    
    # Flight path and velocity parameters
    ALPHA = 2.86             # in degrees
    
    VY_MIN = -50.0           # in km/hr
    VY_MAX = 50.0            # in km/hr
    BIN_SIZE_VY = 1.0        # in km/hr
    BINS_VY = 100
    
    VZ_MIN = -20.0           # in km/hr
    VZ_MAX = 20.0            # in km/hr
    BIN_SIZE_VZ = 1.0        # in km/hr
    BINS_VZ = 40
    
    # Mass of plane
    M = 1.0                  # in kg
    
    # Runway parameters and landing parameters
    Y_MAX_RUNWAY = 0.04      # in km
    Y_MIN_RUNWAY = -0.04     # in km
    Z_LAND_TOL = 0.02        # in km
    VY_LAND_TOL_MAX = 20.0   # in km/hr
    VY_LAND_TOL_MIN = -20.0  # in km/hr
    VZ_LAND_TOL_MIN = -10.0  # in km/hr
    
    # Wind parameters
    VW_SIGMA = 1.0           # in km/hr
    VW = 20.0                # in km/hr
    VW_MAX = 25.0            # in km/hr
    VW_MIN = -25.0           # in km/hr
    BIN_SIZE_VW = 1.0        # in km/hr
    BINS_VW = 50
    
    # Action parameters
    DELTA_VZ_MAX = 35.0      # in km/hr/s
    DELTA_VZ_MIN = -35.0     # in km/hr/s
    BIN_SIZE_DELTA_VZ = 0.35 # in km/hr/s
    BINS_DELTA_VZ = 200
    
    DELTA_VY_MAX = 35.0      # in km/hr/s
    DELTA_VY_MIN = -35.0     # in km/hr/s
    BIN_SIZE_DELTA_VY = 0.35 # in km/hr/s
    BINS_DELTA_VY = 200
    
    # Set the simulation starting parameters here
    START_T = T_MAX          # in sec
    START_Y = 0.0            # in km
    START_Z = Z_MAX          # in km
    START_VY = 0.0           # in km/hr
    START_VZ = -13.0         # in km/hr
    START_VW = VW            # in km/hr
    
    # Set the penalty parameters here
    PENALTY_CRASH = -1e8
    PENALTY_OUTSIDE_RADAR = -1e8
    PENALTY_MISSED_LANDING = -1e3
    PENALTY_DV = -10
    PENALTY_RUNWAY = -10