
from classes.model_parameters import MP
from classes.test_distribution_plotter import PlotTestDistribution
from classes.animate_distribution import AnimateDistribution
from functions.intensity_distribution import get_intensity_distr
from scipy.optimize import minimize
import time
import numpy as np


class TNCModel:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self):
        # To keep track of the iterations
        self.counter = 0

        # Parameters
        self.name = 'TNC'
        self.refl = False
        self.save_fig = True
        self.save_log = True

        if self.save_log:
            self.data = []

        print("Welcome! You are using a TNC optimiser.")
        print("Reflections: ", self.refl)

        time.sleep(1)

        # Objective function. We want to maximise this
        self.result = minimize(self.obj_fun, MP.INITIAL_GUESS_LAMP_LOCS, method='TNC')

        # What is the result of the optimisation?
        print(self.result)

    def obj_fun(self, vars):
        """
        Objective function to be minimised. This maximises the minimum of the light distribution.
        """

        # Calculate current intensity distribution
        light_intensity, minimum, minimum_coordinates = get_intensity_distr(vars, refl=self.refl)

        if self.save_log:
            self.data.append([light_intensity, minimum, minimum_coordinates])

        # Since we want to maximise with a minimisation approach we need to minimise the negative function value
        print("Iteration: ", self.counter, " Variables: ", vars, " Minimum: ", minimum)
        self.counter += 1

        return -minimum


if __name__ == '__main__':

    model = TNCModel()
    PlotTestDistribution(model.result.x, model.name, refl=model.refl, save_fig=model.save_fig, fig_name=model.name)
    #AnimateDistribution(model.data, model.name, True, model.name)