from classes.model_parameters import MP
from classes.test_distribution_plotter import PlotTestDistribution
from classes.animate_distribution import AnimateDistribution
from functions.intensity_distribution import get_intensity_distr
from functions.cost import cost
from scipy.optimize import minimize, BFGS, LinearConstraint, SR1
import time

class TrustConstrModel:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self):

        # To keep track of the iterations
        self.counter = 0

        # Parameters
        self.name = 'Trust-Constr'
        self.refl = True
        self.save_fig = True
        self.save_log = False
        self.constrained = True

        if self.save_log:
            self.data = []

        if self.constrained:
            self.constraints = LinearConstraint(MP.CONSTRAINT_MAT, MP.LOWER_BOUND, MP.UPPER_BOUND)
        else:
            self.constraints = ()

        print("Welcome! You are using a trust-constr optimiser.")
        print("Reflections: ", self.refl)
        print("Constraints: ", self.constrained)

        time.sleep(1)
        # Objective function. We want to maximise this

        self.result = minimize(self.obj_fun, MP.INITIAL_GUESS_LAMP_LOCS, method='trust-constr', jac='3-point',
                            constraints=self.constraints, hess=BFGS(exception_strategy='damp_update'))

        # What is the result of the optimisation?
        print(self.result)

    def obj_fun(self, vars):
        """
        Objective function to be minimised. This maximises the ratio between the minimum light intensity and total cost.
        """

        # Calculate current intensity distribution
        light_intensity, minimum, minimum_coordinates = get_intensity_distr(vars, refl=self.refl)

        # Calculate total cost of given distribution
        total_cost = cost(vars)

        # Since we want to maximise with a minimisation approach we need to minimise the negative function value
        print("Iteration: ", self.counter, " Variables: ", vars, " Minimum: ", minimum, " Cost: ", total_cost)
        self.counter += 1

        return - ((MP.WEIGHT_LIGHT * minimum) / (MP.WEIGHT_COST * total_cost))


if __name__ == '__main__':

    model = TrustConstrModel()
    PlotTestDistribution(model.result.x, model.name, refl=model.refl, save_fig=model.save_fig, fig_name=model.name,
                         constrained=model.constrained, cost_subsystem=True)
    #AnimateDistribution(model.data, model.name, True, model.name)