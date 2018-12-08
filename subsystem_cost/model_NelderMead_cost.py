from classes.model_parameters import MP
from classes.test_distribution_plotter import PlotTestDistribution
from classes.animate_distribution import AnimateDistribution
from functions.intensity_distribution import get_intensity_distr
from functions.cost import cost_obj_fun
from scipy.optimize import minimize
import time


class NelderMeadModel:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self):
        # To keep track of the iterations
        self.counter = 0

        # Parameters
        self.name = 'Nelder-Mead'
        self.refl = True
        self.save_fig = False
        self.save_log = False

        if self.save_log:
            self.data = []

        print("Welcome! You are using a Nelder-Mead optimiser.")
        print("Reflections: ", self.refl)

        time.sleep(1)

        # Objective function. We want to maximise this
        self.result = minimize(self.obj_fun, MP.INITIAL_SOLUTION, method='Nelder-Mead', tol=None,
                               callback=None, options={'disp': True, 'adaptive': True, 'maxiter': 5000})

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

    model = NelderMeadModel()

    PlotTestDistribution(model.result.x, model.name, refl=model.refl, save_fig=model.save_fig, fig_name=model.name,cost_subsystem= True)
    #AnimateDistribution(model.data, model.name, True, model.name)