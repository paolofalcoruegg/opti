import numpy as np
from scipy.optimize import NonlinearConstraint, BFGS

class MP:
    """
    Enum to hold some of the Model Parameters
    """

    """ 
    Global Parameters
    """

    # Discretisation step
    DXY = 0.01

    # Room geometry
    ROOM_LENGTH = 4
    ROOM_WIDTH = 3
    ROOM_HEIGHT = 2.3
    F_PLUG_POSITION = [2.3, 0.05]
    S_PLUG_POSITION = [3.95, 2]


    # Number of lamps
    N_LAMPS = 3

    # Parameters
    LAMP_EFFICIENCY = 0.8
    LAMP_RADII = [0.1, 0.2, 0.1]

    POWER_SCALING_FACTOR = 1
    LAMP_POW = [50, 120, 50]
    LAMP_POW = np.array(LAMP_POW) * POWER_SCALING_FACTOR

    # Albedo
    ALBEDO = 0.5
    BOUNCES = 3

    # Plot parameters
    N_LEVELS = 20

    """
    Light Quality Subsystem
    """

    # Initial lamp location guess (design variables: [x1, y1, x2, y2, x3, y3])
    INITIAL_GUESS_LAMP_LOCS = np.array([0.68978269, 0.98767149, 1.78447148, 2.79305784, 3.66072114, 2.4])

    # Linear Constraint Matrix
    CONSTRAINT_MAT = [[1, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1]]

    # Lamp 1: Bed: Bound Constraints (x1, y1)
    G1 = [LAMP_RADII[0], 2.3 - LAMP_RADII[0]]
    G2 = [LAMP_RADII[0], 1.5 - LAMP_RADII[0]]

    # Lamp 2: Floor: Bound Constraints (x2, y2)
    G3 = [0.4 + LAMP_RADII[1], 2.3 - LAMP_RADII[1]]
    G4 = [0.9 + LAMP_RADII[1], 3 - LAMP_RADII[1]]

    # Lamp 3: Desk: Bound Constraints (x3, y3)
    G5 = [2.3 + LAMP_RADII[2], 4 - LAMP_RADII[2]]
    G6 = [1.1 + LAMP_RADII[2], 3 - LAMP_RADII[2]]

    CONSTRAINTS = [G1, G2, G3, G4, G5, G6]

    # Linear Constraint Bounds
    LOWER_BOUND = [constraint[0] for constraint in CONSTRAINTS]
    UPPER_BOUND = [constraint[1] for constraint in CONSTRAINTS]

    """
    Cost Subsystem
    """

    # Cost
    CABLE_COST = 2
    WORK_COST = 40
    ENERGY_COST = 0.12
    AVG_HOURS_PER_YEAR = float(2500 / 1000)
    INVESTMENT_FACTOR = 1
    # Bea's add
    # Initial characteristics for lamps
    INITIAL_SOLUTION = np.array([0.68978269, 0.98767149, 1.78447148, 2.79305784, 3.66072114, 2.22234, 0.2])

    # Efficiency, in a range from 0 to 1
    G7 = [0.2, 1]

    CONSTRAINT_MAT_EXT = [[1, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0, 1]]

    # Add all constrains to limit all variables to 0

    CONSTRAINTS_EXT = [G1, G2, G3, G4, G5, G6, G7]

    # Linear Constraint Bounds
    LOWER_BOUND_EXT = [constraint[0] for constraint in CONSTRAINTS_EXT]
    UPPER_BOUND_EXT = [constraint[1] for constraint in CONSTRAINTS_EXT]

    """
    System Level

    """

    # Weight of different subsystems
    WEIGHT_LIGHT = 1
    WEIGHT_COST = 1

"""
FUNCTIONAL CONSTRAINTS
"""

def functional_constraint(variables):
    c_cable_tot = 0

    # Power would need to be 50 or 120 depending on which lamp it is reffereing to
    total_power = sum(MP.LAMP_POW)

    for i in range(3):
        c_cable_tot += (abs(variables[2 * i]) + abs(variables[2 * i + 1])) + 1.6
        c_cable_tot = c_cable_tot * MP.CABLE_COST

    lamp_efficiency = variables[6]
    c_operation = (total_power / lamp_efficiency) * MP.AVG_HOURS_PER_YEAR * MP.ENERGY_COST
    c_lamp = (lamp_efficiency / 0.2)
    c_tot_lamp_cost = MP.N_LAMPS * c_lamp
    c_work = np.log(MP.N_LAMPS) * MP.WORK_COST
    c_initial = (c_cable_tot + c_tot_lamp_cost + c_work)

    return c_initial - MP.INVESTMENT_FACTOR * c_operation