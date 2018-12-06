import numpy as np
from classes.model_parameters import MP
from classes.room import Room
from scipy.optimize import minimize
from functions.cost import cost_obj_fun
from classes.test_distribution_plotter import PlotTestDistribution


class Model:
    """
    Class for optimization of the cost
    """

    def __init__(self, method):

        # To keep track of the iterations
        self.counter = 0
        self.varsnumber = 4 #each iteration is going to give two values (x,y for three times and c1,c2 for characteristic
        # These will restult in 8 variables = 6 position, and characteristic in 2 (cost and efficiency)

        # Objective function. We want to maximise this
        self.result = minimize(self.obj_fun, MP.INITIAL_SOLUTION, method=method)

        # What is the result of the optimisation?
        print(self.result)


    def obj_fun(self, variables):
        """
        Cost objective function. Vars is [x1, y1, x2, y2, x3, y3, c]
        Where c is equal for the three lamps and is equal to the the characteristics
        of lamp composed by price and efficiency
        Call the function cost
        """
        # Calculate current intensity distribution
        c_tot = cost_obj_fun(variables)

        print("Iteration: ", self.counter)
        self.counter += 1

        return c_tot


if __name__ == '__main__':

    # Start Hand engine
    model = Model('TNC')

    #PlotTestDistribution(model.result.x, "TNC")
    #PlotTestDistribution((1,1,2,2,3,3), "TNC")


    PlotTestDistribution(model.result.x, "TNC", False, False, '', True, True)

