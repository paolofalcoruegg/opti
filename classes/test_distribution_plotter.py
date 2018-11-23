import numpy as np
import numpy.ma as ma
from classes.model_parameters import MP
from functions.intensity_distribution import get_intensity_distr
import matplotlib.pyplot as plt


class PlotTestDistribution:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self,
                 lamp_locs = (1, 1, 1.5, 2, 3, 2.5),
                 name='',
                 refl=False,
                 save_fig=False,
                 fig_name='',
                 constrained=False):

        # These cannot be taken from the enum, as they vary upon each instatiation
        self.lamp_locs = lamp_locs
        self.name = name
        self.refl = refl
        self.save_fig = save_fig
        self.fig_name = fig_name
        self.constrained = constrained

        # Plot
        self.plot_intensity_distr()

    def plot_intensity_distr(self):
        """
        Calculates the intensity distribution within a room with n number of light sources
        """

        light_intensity, minimum, minimum_coordinates = get_intensity_distr(self.lamp_locs, self.refl)

        # Plot background image of room
        img = plt.imread("../classes/room_outline.png")
        plt.imshow(img, extent=[0, MP.ROOM_LENGTH / MP.DXY, 0, MP.ROOM_WIDTH / MP.DXY])

        # Plot intensity distribution
        plot = plt.contourf(light_intensity, MP.N_LEVELS, cmap='plasma', alpha=0.75, antialiased=True)

        # Plot global minimum
        plt.plot(minimum_coordinates[1], minimum_coordinates[0], 'ro', markersize=12)

        # Layout & Titles
        plt.title(self.name + " Optimisation, Refl: " + str(self.refl) + ", Cons: " + str(self.constrained)
                  + ", Min: " + str(round(minimum, 2)))
        plt.xlabel('Room X-Position (cm)')
        plt.ylabel('Room Y-Position (cm)')

        # Export figure
        if self.save_fig:
            plt.savefig(self.fig_name + str(self.refl) + str(self.constrained) + '.svg', format='svg', dpi=1200)

        # Show figure
        plt.show()

if __name__ == '__main__':

    PlotTestDistribution((1, 1, 1.5, 2, 3, 2.5), '', True)