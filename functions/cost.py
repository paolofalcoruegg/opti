from classes.model_parameters import MP
import numpy as np

def cost(vars, pow_var=False):
    """
    Cost objective function. Vars is [x1, y1, x2, y2, x3, y3]
    """
    c_cable_tot = 0

    for i in range(MP.N_LAMPS):
        # cables come from the ceiling(3m) so add 1.4 to reach 1.6 m ideal position)
        # c_cable_tot += np.sqrt(vars[2 * i] ** 2 + vars[2 * i + 1] ** 2)
        # new cable price based on L shape
        c_cable_tot += (abs(vars[2 * i]) + abs(vars[2 * i + 1])) + 1.6

    c_cable_tot = c_cable_tot * MP.CABLE_COST

    c_lamp = MP.N_LAMPS * MP.LAMP_COST

    c_work = np.log(MP.N_LAMPS) * MP.WORK_COST

    # Note to Bea: This was just a little experiment. Assume pow_var is always false
    if not pow_var:
        c_operation = sum(MP.LAMP_POW) * MP.AVG_HOURS_PER_YEAR * MP.ENERGY_COST
    else:
        c_operation = (vars[6] + vars[7] + vars[8]) * MP.AVG_HOURS_PER_YEAR * MP.ENERGY_COST

    c_tot = c_cable_tot + c_lamp + c_work + c_operation

    return c_tot