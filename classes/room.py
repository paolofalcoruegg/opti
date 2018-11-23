import numpy as np
from classes.model_parameters import MP
import numpy.ma as ma

class Room:
    """
    The Room class contains the space in which the lighting optimisation will take place
    """

    def __init__(self, length, width):

        self.x = np.arange(0, length, MP.DXY)
        self.y = np.arange(0, width, MP.DXY)
        self.xx, self.yy = np.meshgrid(self.x, self.y, sparse=True)

