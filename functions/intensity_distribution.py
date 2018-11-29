from classes.model_parameters import MP
from classes.room import Room
import numpy as np
import numpy.ma as ma

def get_intensity_distr(lamp_locs, refl=False):
    """
    Calculates the intensity distribution within a room with n number of light sources
    """

    room = Room(MP.ROOM_LENGTH, MP.ROOM_WIDTH)

    # No reflections
    if not refl:

        for i in range(MP.N_LAMPS):
            # Multiply by discretisation step to be in metres
            distance_to_lamp_n = ((room.xx - lamp_locs[2 * i]) ** 2 + (room.yy - lamp_locs[2 * i + 1]) ** 2)

            # Take out the value that are less than a radius away from the light source
            distance_to_lamp_n_filtered = ma.masked_less(np.sqrt(distance_to_lamp_n), MP.LAMP_RADII[i])

            if i == 0:
                # Initialise the light intensity array
                light_intensity = np.zeros_like(distance_to_lamp_n_filtered)

            # Find light intensity distribution
            light_intensity_n = ((MP.LAMP_EFFICIENCY * MP.LAMP_POW[i]) /
                                 (4 * np.pi)) / (distance_to_lamp_n_filtered * MP.DXY)

            light_intensity += light_intensity_n

        minimum = np.amin(light_intensity)
        minimum_coordinates = np.unravel_index(np.argmin(light_intensity), light_intensity.shape)

        return light_intensity, minimum, minimum_coordinates

    # With reflections
    elif refl:

        initialised = False

        # The first loop takes care of wall reflections
        for i in range(- MP.BOUNCES // 2, MP.BOUNCES // 2 + 1):
            # The second loop takes care of the three different lamps
            for j in range(MP.N_LAMPS):

                x_jk = 0.5 * (1 + (-1) ** i) * lamp_locs[2 * j] + \
                       0.5 * (1 - (-1) ** i) * (MP.ROOM_LENGTH - lamp_locs[2 * j])
                y_jk = 0.5 * (1 + (-1) ** i) * lamp_locs[2 * j + 1] + \
                       0.5 * (1 - (-1) ** i) * (MP.ROOM_WIDTH - lamp_locs[2 * j + 1])

                distance_to_lamp_n = ((room.xx - (x_jk - MP.ROOM_LENGTH * i)) ** 2 +
                                      (room.yy - (y_jk - MP.ROOM_WIDTH * i)) ** 2)

                # Take out the value that are less than a radius away from the light source
                distance_to_lamp_n_filtered = ma.masked_less(np.sqrt(distance_to_lamp_n), MP.LAMP_RADII[j])

                # Initialise the light intensity array
                if not initialised:
                    light_intensity = np.zeros_like(distance_to_lamp_n_filtered)
                    initialised = True

                # Find light intensity distribution
                light_intensity_n = ((MP.ALBEDO ** (abs(2 * i))) * (MP.LAMP_EFFICIENCY * MP.LAMP_POW[j]) /
                                     (4 * np.pi)) / (distance_to_lamp_n_filtered * MP.DXY)

                # Increment light intensity array
                light_intensity += light_intensity_n

        minimum = np.amin(light_intensity)
        minimum_coordinates = np.unravel_index(np.argmin(light_intensity), light_intensity.shape)

        return light_intensity, minimum, minimum_coordinates
