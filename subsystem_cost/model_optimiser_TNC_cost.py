
from classes.model_parameters import MP
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
        # Number of set of variables (Iterations 0 to 2 will give two solutions, x and y for each of the lamps
        # Iteration 3 will give one solution, efficiency
        self.varsnumber = 4

        print("You are using a Nelder-Mead optimiser.")

        # Set the minimizer
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
        # Calculate current cost
        c_tot = cost_obj_fun(variables)

        print("Iteration: ", self.counter, "Positions and efficiency", variables, "total cost", c_tot)
        self.counter += 1

        return c_tot


if __name__ == '__main__':

    # Start Hand engine
    model = Model('TNC')


    PlotTestDistribution(model.result.x, "TNC", False, False, '', True, True)

