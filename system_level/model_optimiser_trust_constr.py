from classes.model_parameters import MP, functional_constraint
from classes.test_distribution_plotter import PlotTestDistribution
from classes.animate_distribution import AnimateDistribution
from functions.intensity_distribution import get_intensity_distr
from functions.cost import cost_obj_fun
from scipy.optimize import minimize, BFGS, LinearConstraint, NonlinearConstraint
import numpy as np
import time

class TrustConstrModel:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self, weight_light = False):

        # To keep track of the iterations
        self.counter = 0

        # Parameters
        self.name = 'Trust-Constr'
        self.refl = True
        self.save_fig = True
        self.save_log = False
        self.constrained = True

        if not weight_light:
            self.weight_light = MP.WEIGHT_LIGHT
        else:
            self.weight_light = weight_light

        if self.save_log:
            self.data = []

        if self.constrained:
            self.constraints = (LinearConstraint(MP.CONSTRAINT_MAT_EXT, MP.LOWER_BOUND_EXT, MP.UPPER_BOUND_EXT),
                                NonlinearConstraint(functional_constraint, -np.inf, 0, jac='cs', hess=BFGS()))
        else:
            self.constraints = ()

        print("Welcome! You are using a trust-constr optimiser.")
        print("Reflections: ", self.refl)
        print("Constraints: ", self.constrained)

        time.sleep(1)
        # Objective function. We want to maximise this

        self.result = minimize(self.obj_fun, MP.INITIAL_SOLUTION, method='trust-constr', jac='3-point',
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
        total_cost = cost_obj_fun(vars)

        # Since we want to maximise with a minimisation approach we need to minimise the negative function value
        print("Iteration: ", self.counter, " Variables: ", [round(var, 2) for var in vars], " Minimum: ", round(minimum, 2), " Cost: ",
              round(total_cost, 2))
        self.counter += 1

        return (1 - self.weight_light) * total_cost - self.weight_light * minimum


if __name__ == '__main__':

    #model = TrustConstrModel()
    #PlotTestDistribution(model.result.x, model.name, refl=model.refl, save_fig=model.save_fig, fig_name=model.name,
     #                    constrained=model.constrained, cost_subsystem=True)

    filename = 'pareto.txt'
    file = open(filename, 'w')

    weight_light_range = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for weight in weight_light_range:
        model = TrustConstrModel(weight)
        file.write('Light Weight: ' + str(weight) + ' Optimum: ' + str(model.result.x))
        file.write('\n')
        print("Now solving for weight: ", weight)

    file.close()



    #AnimateDistribution(model.data, model.name, True, model.name)