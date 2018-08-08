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


class InputController(object):
    """
    Binds a defined button input to a single physics object
    """

    def __init__(self, input_objects: list, physics_object: PhysicsObject):
        self.input_objects = input_objects
        self.physics_object = physics_object

        # Disables the controller's forces for all objects except the bound one
        for input_object in self.input_objects:
            input_object.force.item_array = np.zeros(
                physics_object.physics_controller.n_objects)
            input_object.force.item_array[self.physics_object.index] = 1

    def read_input(self):
        for input_object in self.input_objects:
            try:
                for button in input_object.button:
                    if pyxel.btn(button):
                        self.physics_object.physics_controller. \
                            temporary_forces.append(
                            input_object.force)
                        break
            except TypeError:
                if pyxel.btn(input_object.button):
                    self.physics_object.physics_controller.temporary_forces.append(
                        input_object.force
                    )
