import numpy as np
from classes.model_parameters import MP
from classes.room import Room
from scipy.optimize import minimize
from classes.test_distribution_plotter import PlotTestDistribution


class Model:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self):

        # To keep track of the iterations
        self.counter = 0

        # Objective function. We want to maximise this
        self.result = minimize(self.cost_obj_fun, MP.INITIAL_GUESS_LAMP_LOCS, method='TNC')

        # What is the result of the optimisation?
        print(self.result)

    def cost_obj_fun(self, vars, debug=False):
        """
        Cost objective function. Vars is [x1, y1, x2, y2, x3, y3]
        """
        c_cable_tot = 0

        for i in range(MP.N_LAMPS):
            #cables come from the ceiling(3m) so add 1.4 to reach 1.6 m ideal position)
            #c_cable_tot += np.sqrt(vars[2 * i] ** 2 + vars[2 * i + 1] ** 2)
            #new cable price based on L shape
            c_cable_tot += (abs(vars[2 * i]) + abs(vars[2 * i + 1])) + 1.6

        c_cable_tot = c_cable_tot * MP.CABLE_COST

        c_lamp = MP.N_LAMPS * MP.LAMP_COST

        c_work = np.log(MP.N_LAMPS) * MP.WORK_COST

        c_operation = sum(MP.LAMP_POW) * MP.AVG_HOURS_PER_YEAR * MP.ENERGY_COST

        c_tot = c_cable_tot + c_lamp + c_work + c_operation

        print("Iteration: ", self.counter, " with positions: ", vars, " with total cost: ", c_tot)
        self.counter += 1

        if debug:
            print("This is the cable cost: ", c_cable_tot)
            print("This is the lamp cost: ", c_lamp)
            print("This is the work cost: ", c_work)
            print("This is the operation cost: ", c_operation)
            print("This is the total cost: ", c_tot)

        return c_tot

if __name__ == '__main__':

    # Start Hand engine
    model = Model()

    #PlotTestDistribution(model.result.x, "TNC")
    #PlotTestDistribution((1,1,2,2,3,3), "TNC")


    PlotTestDistribution(model.result.x, "TNC", False, False, '', True, True)

