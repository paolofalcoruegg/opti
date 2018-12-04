import numpy as np
import numpy.ma as ma
from classes.model_parameters import MP
from functions.intensity_distribution import get_intensity_distr
from functions.cost import cost
import matplotlib.pyplot as plt
import operator as op


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
                 constrained=False,
                 cost_subsystem=False):

        # These cannot be taken from the enum, as they vary upon each instatiation
        self.lamp_locs = lamp_locs
        self.name = name
        self.refl = refl
        self.save_fig = save_fig
        self.fig_name = fig_name
        self.constrained = constrained
        self.cost_subsystem = cost_subsystem

        # Define plugs position
        self.firstplug_position = MP.F_PLUG_POSITION
        self.secondplug_position = MP.S_PLUG_POSITION

        # Plot
        if not self.cost_subsystem:
            self.plot_intensity_distr()
        else:
            self.plot_cable_distribution()

    def plot_intensity_distr(self):
        """
        Calculates the intensity distribution within a room with n number of light sources
        """

        light_intensity, minimum, minimum_coordinates = get_intensity_distr(self.lamp_locs, self.refl)

        # Fill masked areas (lamps) with maximum value
        light_intensity = ma.filled(light_intensity, np.amax(light_intensity))

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # Plot background image of room
        if not self.constrained:
            img = plt.imread("../classes/room_outline.png")
        else:
            img = plt.imread("../classes/room_outline_constr.png")

        ax.imshow(img, extent=[0, MP.ROOM_LENGTH / MP.DXY, 0, MP.ROOM_WIDTH / MP.DXY])

        # Plot intensity distribution
        ax.contourf(light_intensity, MP.N_LEVELS, cmap='plasma', alpha=0.75, antialiased=True)

        # Plot global minimum
        ax.plot(minimum_coordinates[1], minimum_coordinates[0], 'ro', markersize=12)

        # Layout & Titles
        plt.suptitle(self.name + " Optimisation", fontweight='bold')
        plt.title("Reflections: " + str(self.refl) + ", Constraints: " + str(self.constrained)
                  + ", Minimum: " + str(round(minimum, 2)), fontsize='large')
        plt.xlabel('Room X-Position (cm)')
        plt.ylabel('Room Y-Position (cm)')

        # Export figure
        if self.save_fig:
            plt.savefig(self.fig_name + str(self.refl) + str(self.constrained) + '.svg', format='svg', dpi=1200)

        # Show figure

        plt.show()

    def plot_cable_distribution(self):
        """
               Calculates the intensity distribution within a room with n number of light sources
               """

        #light_intensity, minimum, minimum_coordinates = get_intensity_distr(self.lamp_locs, self.refl)
        light_intensity, minimum, minimum_coordinates = get_intensity_distr(self.lamp_locs, self.refl)
        total_cost = cost(self.lamp_locs)

        # Fill masked areas (lamps) with maximum value
        light_intensity = ma.filled(light_intensity, np.amax(light_intensity))

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # Plot background image of room
        if not self.constrained:
            img = plt.imread("../classes/room_outline.png")
        else:
            img = plt.imread("../classes/room_outline_constr.png")

        ax.imshow(img, extent=[0, MP.ROOM_LENGTH / MP.DXY, 0, MP.ROOM_WIDTH / MP.DXY])

        # Plot intensity distribution
        ax.contourf(light_intensity, MP.N_LEVELS, cmap='plasma', alpha=0.75, antialiased=True)

        # Plot global minimum
        ax.plot(minimum_coordinates[1], minimum_coordinates[0], 'ro', markersize=12)


        # plot cost
        for i in range(MP.N_LAMPS):

            lamp_position = [self.lamp_locs[2 * i], self.lamp_locs[2 * i + 1]]
            print("lamp_position: ", lamp_position)
            print("position first plug: ", self.firstplug_position)
            print("position second plug: ", self.secondplug_position)
            # distance to first plug and second plang
            d_fp = list(map(op.sub, lamp_position, self.firstplug_position))
            d_sp = list(map(op.sub, lamp_position, self.secondplug_position))
            print("distance from first plug to lamp: ", d_fp)
            print("distance from second plug to lamp: ", d_sp)

            # therefore cable length for L shape
            l_fp = (abs(d_fp[0]) + abs(d_fp[1]))
            l_sp = (abs(d_sp[0]) + abs(d_sp[1]))

            print("cable length to plug 1: ", l_fp)
            print("cable length to plug 2: ", l_sp)

            # Seems to be x1, x2,y1,y2 - look into this
            if l_fp <= l_sp:
                plt.plot([100 * self.firstplug_position[0], 100 * self.lamp_locs[2 * i]],
                         [100 * self.firstplug_position[1], 100 * self.firstplug_position[1]], "grey")
                plt.plot([100 * self.lamp_locs[2 * i], 100 * self.lamp_locs[2 * i]],
                         [100 * self.firstplug_position[1], 100 * self.lamp_locs[2 * i + 1]], "grey")
            else:
                plt.plot([100 * self.secondplug_position[0], 100 * self.lamp_locs[2 * i]],
                         [100 * self.secondplug_position[1], 100 * self.secondplug_position[1]], "grey")
                plt.plot([100 * self.lamp_locs[2 * i], 100 * self.lamp_locs[2 * i]],
                         [100 * self.secondplug_position[1], 100 * self.lamp_locs[2 * i + 1]], "grey")


        # Layout & Titles
        plt.suptitle(self.name + " Optimisation", fontweight='bold')
        plt.title("Constraints: " + str(self.constrained) + ", Minimum: " + str(round(minimum, 2)) +
                  ", Cost: " + str(round(total_cost, 2)), fontsize='large')
        plt.xlabel('Room X-Position (cm)')
        plt.ylabel('Room Y-Position (cm)')
        # Export figure
        if self.save_fig:
            plt.savefig('../plots/' + self.fig_name + str(self.refl) + str(self.constrained) + str(self.cost_subsystem) + 
            	'.svg', format='svg', dpi=1200)

        # Show figure
        plt.show()



if __name__ == '__main__':

    PlotTestDistribution((1, 1, 1.5, 2, 3, 2.5), 'Test', True, False, '', True, True)