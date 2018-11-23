import matplotlib.pyplot as plt
from matplotlib import animation

class AnimateDistribution:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self, data, name='', save_ani=False, ani_name=''):

        light_intensities = []
        minima = []
        minimum_coordinates = []

        for row in data:
            light_intensities.append(row[0])
            minima.append(row[1])
            minimum_coordinates.append(row[2])

        def animate(i):
            ax.clear()
            ax.contourf(light_intensities[i], 4, cmap='plasma')
            ax.plot(minimum_coordinates[i][1], minimum_coordinates[i][0], 'ro', markersize=12)
            ax.set_title(name + ' Iteration: ' + '%03d' % (i) + ' Min: ' + str(round(minima[i],2)))


        fig, ax = plt.subplots()

        interval = 0.25  # in seconds
        ani = animation.FuncAnimation(fig, animate, len(light_intensities), interval=interval, blit=False)

        if save_ani:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

            ani.save(ani_name + '.mp4', writer=writer)

        plt.show()
