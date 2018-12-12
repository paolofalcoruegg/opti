from classes.model_parameters import MP
import numpy as np


def cost_obj_fun(variables):
    """
    Cost objective function. Vars is [x1, y1, x2, y2, x3, y3, e, i]
    Where c is equal for the three lamps and is equal to the the characteristics of lamp composed by price and efficiency
    """
    #Total cable cost is initialised
    c_cable_tot = 0

    # The power is fixed, so the total power is a sum of the power of all the lamps
    total_power = sum(MP.LAMP_POW)

    '''
    There are 7 variables in total
    In a range of 3 - which equals for iterations,  i = 0,1 and 2 will refer to each of the lamps. 
    The code will consider which considers i and i+1 for x, y  
    '''
    #Start the loop to calculate cable length
    for i in range(3):
        #Calcilate total length, including 1.6 m for the height of the lamps in the room.
        c_cable_tot += (abs(variables[2 * i]) + abs(variables[2 * i + 1])) + 1.6
        #Calculate the total price
        c_cable_tot = c_cable_tot * MP.CABLE_COST

    lamp_efficiency = variables[6]
    # Calculate the operation cost in terms of the efficiency
    c_operation = (total_power/lamp_efficiency) * MP.AVG_HOURS_PER_YEAR * MP.ENERGY_COST

    #Calculate the lamp cost in terms of the efficiency
    c_lamp = (lamp_efficiency/0.2)

    # Calculate total lamp cost
    c_tot_lamp_cost = MP.N_LAMPS * c_lamp

    # Calculate work cost
    c_work = np.log(MP.N_LAMPS) * MP.WORK_COST

    #Caltulate the initial cost
    c_initial = (c_cable_tot + c_tot_lamp_cost + c_work)

    #Caltulate total cost
    c_tot = c_initial + c_operation

    return c_tot


