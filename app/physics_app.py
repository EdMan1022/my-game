import random

import numpy as np

import pyxel

from .classes.physics_object import PhysicsObject, PhysicsBox
from .classes.physics_controller import PhysicsController
from .classes.input_object import InputObject, InputController
from .classes import forces


class PhysicsApp(object):
    __slots__ = ('width', 'height', 'x',
                 '_x_update', '_x_speed', 'y', '_y_update', 'y_speed',
                 'key_up', 'key_down', 'key_left', 'key_right', 'fps',
                 '__dict__')

    def __init__(self, width: int = 240, height: int = 180, fps: int=60):
        self.width = width
        self.height = height
        self.fps = fps

        self.x_speed = 1
        self.x_slow = .2
        self.y_speed = 1
        self.y_slow = .5
        self._init_pyxel()

        self.key_up = pyxel.constants.KEY_W
        self.key_down = pyxel.constants.KEY_S
        self.key_left = pyxel.constants.KEY_A
        self.key_right = pyxel.constants.KEY_D

        self.physics_controller = PhysicsController(
            continuous_forces=[],
        )

        self.physics_objects = [
            PhysicsBox(x_i=20, x_dot_1_i=0, y_i=20, y_dot_1_i=0,
                       mass=1, physics_controller=self.physics_controller)
        ]

        self.physics_controller.objects = self.physics_objects
        self.physics_controller.init_physics_arrays()

        control_force = 70.

        self.physics_controller.input_controllers = [
            InputController(
                input_objects=[
                    InputObject(
                        button=pyxel.constants.KEY_W,
                        force=forces.ControlForce(
                            x_value=np.zeros(self.physics_controller.n_objects),
                            y_value=np.full(self.physics_controller.n_objects,
                                            - control_force)
                        )),
                    InputObject(
                        button=pyxel.constants.KEY_S,
                        force=forces.ControlForce(
                            x_value=np.zeros(self.physics_controller.n_objects),
                            y_value=np.full(self.physics_controller.n_objects,
                                            control_force)
                        )),
                    InputObject(
                        button=pyxel.constants.KEY_A,
                        force=forces.ControlForce(
                            x_value=np.full(self.physics_controller.n_objects,
                                            - control_force),
                            y_value=np.zeros(self.physics_controller.n_objects)
                        )),
                    InputObject(
                        button=pyxel.constants.KEY_D,
                        force=forces.ControlForce(
                            x_value=np.full(self.physics_controller.n_objects,
                                            control_force),
                            y_value=np.zeros(self.physics_controller.n_objects)
                        )),
                    InputObject(
                        button=(pyxel.constants.KEY_LEFT_SHIFT,
                                pyxel.constants.KEY_RIGHT_SHIFT),
                        force=forces.BrakeForce(
                            value=np.full(self.physics_controller.n_objects,
                                          2 * control_force)
                        ))
                ],
                physics_object=self.physics_controller.objects[0]
            )
        ]

    def _init_pyxel(self):
        pyxel.init(self.width, self.height, fps=self.fps)

    def update(self):
        self.physics_controller.update()

    def draw(self):
        pyxel.cls(0)

        for obj in self.physics_objects:
            obj.draw(self)

        # pyxel.text(10, 10, str(self.physics_controller.current_time), 5)
        pyxel.text(10, 30, str(self.physics_controller.acted_temporary_forces),
                   5)
        pyxel.text(10, 50, str(self.physics_objects), 5)
        pyxel.text(10, 70, str(pyxel._app._key_state), 5)

    def run(self):
        pyxel.run(self.update, self.draw)
