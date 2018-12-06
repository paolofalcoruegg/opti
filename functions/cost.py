from classes.model_parameters import MP
import numpy as np


def cost_obj_fun(variables):
    """
    Cost objective function. Vars is [x1, y1, x2, y2, x3, y3, e, i]
    Where c is equal for the three lamps and is equal to the the characteristics of lamp composed by price and efficiency
    """
    c_cable_tot = 0
    c_operation = 0
    lamp_efficiency =0


    # Power would need to be 50 or 120 depending on which lamp it is reffereing to
    total_power = sum(MP.LAMP_POW)
    print (total_power)

    '''
    There are 7 variables in total, in a range of 4 iterations of i (0,1,2,3), where for 0,1,2 is for lamp  
    which considers i and i+1 for x, y 
    The iteration 3 is for the efficiency, taking out i 
    '''

    for i in range(3):
        c_cable_tot += (abs(variables[2 * i]) + abs(variables[2 * i + 1])) + 1.6
        #print("1", c_cable_tot)
        c_cable_tot = c_cable_tot * MP.CABLE_COST
        #print("2", c_cable_tot)

    # The total lamp cost will be the sum of the cost of each map from the characteristics.
    lamp_efficiency = variables[6]
    c_operation = (total_power/lamp_efficiency) * MP.AVG_HOURS_PER_YEAR * MP.ENERGY_COST
    #print ("3", lamp_efficiency)

    c_lamp = (lamp_efficiency/0.2)
    c_tot_lamp_cost = MP.N_LAMPS * c_lamp
    c_work = np.log(MP.N_LAMPS) * MP.WORK_COST

    c_initial = (c_cable_tot + c_tot_lamp_cost + c_work)
    c_tot = c_initial + c_operation

    print("Solution with positions: ", variables,
          "initial cost ", c_initial,
          "of which total cable cost", c_cable_tot,
          "and total lamp cost ", c_tot_lamp_cost,
          "cost of operation", c_operation,
          "with total cost: ", c_tot)


    return c_tot


