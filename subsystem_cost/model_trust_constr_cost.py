from classes.model_parameters import MP, functional_constraint
from classes.test_distribution_plotter import PlotTestDistribution
from functions.cost import cost_obj_fun
from scipy.optimize import minimize, BFGS, LinearConstraint, NonlinearConstraint
import time
import numpy as np

class TrustConstrModel:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self):

        # To keep track of the iterations
        self.counter = 0

        # Parameters
        self.name = 'Trust-Constr'
        self.refl = False
        self.save_fig = False
        self.save_log = False
        self.constrained = True

        if self.save_log:
            self.data = []

        if self.constrained:
            self.constraints = (LinearConstraint(MP.CONSTRAINT_MAT_EXT, MP.LOWER_BOUND_EXT, MP.UPPER_BOUND_EXT),
                                NonlinearConstraint(functional_constraint, -np.inf, 0, jac='cs', hess=BFGS()))
        else:
            self.constraints = ()

        print("You are using a trust-constr optimiser.")
        print("Constraints: ", self.constrained)

        time.sleep(1)
        # Objective function. We want to maximise this
        self.result = minimize(self.obj_fun, MP.INITIAL_SOLUTION, method='trust-constr', jac='3-point',
                               constraints=self.constraints, hess=BFGS(exception_strategy='damp_update'))

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

    model = TrustConstrModel()
    PlotTestDistribution(model.result.x, model.name, refl=model.refl, save_fig=model.save_fig, fig_name=model.name,
                         constrained=model.constrained, cost_subsystem=True)