import numpy as np
import pyxel

from .physics_object import PhysicsObject
from .forces import Force


class InputObject(object):
    """
    Maps a force instance to a button press
    """

    def __init__(self, button, force: Force):
        self.button = button
        self.force = force


