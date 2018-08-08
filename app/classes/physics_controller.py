from time import time
import numpy as np


class PhysicsController(object):
    __slots__ = (
        'start_time', 'current_time', 'previous_time', 'objects',
        'dt', 'mass_array', 'x_array', 'y_array', 'x_dot_1_array',
        'y_dot_1_array', 'x_dot_2_array', 'y_dot_2_array', 'gravity',
        'air_resistance', 'continuous_forces', 'temporary_forces',
        'x_dot_1_sign_array', 'y_dot_1_sign_array',
        'n_objects', 'input_controllers', 'acted_temporary_forces',
        'truncate_value', 'prev_x_dot_2_array', 'prev_y_dot_2_array'
    )

    def __init__(self, objects: list=None, continuous_forces: list=None,
                 temporary_forces: list=None, truncate_value: float=0.1):

        self.start_time = time()
        self.current_time = self.start_time
        self.previous_time = self.start_time
        self.objects = objects
        self.truncate_value = truncate_value

        self.dt = None

        self.mass_array = None

        self.n_objects = None

        self.x_array = None
        self.y_array = None

        self.x_dot_1_array = None
        self.x_dot_1_sign_array = None
        self.y_dot_1_array = None
        self.y_dot_1_sign_array = None

        self.x_dot_2_array = None
        self.prev_x_dot_2_array = None
        self.y_dot_2_array = None
        self.prev_y_dot_2_array = None

        self.input_controllers = None

        if not continuous_forces:
            continuous_forces = []
        if not temporary_forces:
            temporary_forces = []

        self.continuous_forces = continuous_forces
        self.temporary_forces = temporary_forces
        self.acted_temporary_forces = []

        if self.objects:
            self.init_physics_arrays()

    def init_physics_arrays(self):
        """
        Creates numpy arrays to track the physics values of the objects

        :return:
        """
        self.n_objects = len(self.objects)

        self.mass_array = np.ndarray(shape=self.n_objects)

        self.x_array = np.ndarray(shape=self.n_objects)
        self.y_array = np.ndarray(shape=self.n_objects)

        self.x_dot_1_array = np.ndarray(shape=self.n_objects)
        self.y_dot_1_array = np.ndarray(shape=self.n_objects)

        self.x_dot_1_sign_array = np.ndarray(shape=self.n_objects)
        self.y_dot_1_sign_array = np.ndarray(shape=self.n_objects)

        self.x_dot_2_array = np.zeros(shape=self.n_objects)
        self.y_dot_2_array = np.zeros(shape=self.n_objects)

        for i, p_object in enumerate(self.objects):
            p_object.index = i
            p_object.physics_controller = self
            self.mass_array[i] = p_object.mass
            self.x_array[i] = p_object.x_i
            self.y_array[i] = p_object.y_i
            self.x_dot_1_array[i] = p_object.x_dot_1_i
            self.y_dot_1_array[i] = p_object.y_dot_1_i

    def clear_old_forces(self):
        self.acted_temporary_forces = []

    def get_time(self):
        self.current_time = time()
        self.dt = self.current_time - self.previous_time
        self.previous_time = self.current_time

    def resolve_signs(self):
        self.x_dot_1_sign_array = np.full(self.n_objects, -1.)
        self.y_dot_1_sign_array = np.full(self.n_objects, -1.)

        self.x_dot_1_sign_array[self.x_dot_1_array > 0] = 1.
        self.y_dot_1_sign_array[self.y_dot_1_array > 0] = 1.

    def resolve_inputs(self):
        for input_controller in self.input_controllers:
            input_controller.read_input()

    def resolve_forces(self):

        for force in self.continuous_forces:
            force.act(self)

        for force in self.temporary_forces:
            force.act(self)
        self.acted_temporary_forces = self.temporary_forces
        self.temporary_forces = []

    def resolve_accelerations(self):
        self.x_dot_1_array = self.x_dot_1_array + (self.dt * self.x_dot_2_array)
        self.y_dot_1_array = self.y_dot_1_array + (self.dt * self.y_dot_2_array)

        self._truncate_near_zero()

    def clear_accelerations(self):

        self.prev_x_dot_2_array = self.x_dot_2_array
        self.prev_y_dot_2_array = self.y_dot_2_array

        self.x_dot_2_array = np.zeros(shape=self.n_objects)
        self.y_dot_2_array = np.zeros(shape=self.n_objects)

    def _truncate_near_zero(self):
        self.x_dot_1_array[
            abs(self.x_dot_1_array) < self.truncate_value
        ] = 0

        self.y_dot_1_array[
            abs(self.y_dot_1_array) < self.truncate_value
            ] = 0

    @property
    def stopped_array(self):
        return (abs(self.x_dot_1_array) + abs(self.y_dot_1_array)) < self.truncate_value

    @property
    def x_stopped_array(self):
        return self.x_dot_1_array < self.truncate_value

    def resolve_motion(self):
        self.x_array = self.x_array + (self.dt * self.x_dot_1_array)
        self.y_array = self.y_array + (self.dt * self.y_dot_1_array)

    def update(self):

        self.clear_old_forces()

        self.get_time()
        self.resolve_signs()
        self.resolve_inputs()
        self.resolve_forces()
        self.resolve_accelerations()
        self.resolve_motion()

        self.clear_accelerations()
