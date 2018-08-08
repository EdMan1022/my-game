from .physics_controller import PhysicsController


class Force(object):

    def __init__(self, name='force', item_array=None):
        self.item_array = item_array
        self.name = name

    def __repr__(self):
        return "{}: {}\n".format(self.name, self.representation)

    @property
    def representation(self):
        return 'Base'


class Gravity(Force):
    __slots__ = 'y_dot_2'
    name = 'gravity'

    def __init__(self, y_dot_2=-9.8):
        super(Gravity, self).__init__()
        self.y_dot_2 = y_dot_2

    def act(self, pc):
        pc.y_dot_2_array = pc.y_dot_2_array + self.y_dot_2

    @property
    def representation(self):
        return self.y_dot_2


class AirResistance(Force):
    __slots__ = 'rho', 'x_dot_2', 'y_dot_2'
    name = 'air_resistance'

    def __init__(self, rho: float = 1.5):
        super(AirResistance, self).__init__()
        self.rho = rho

        self.x_dot_2 = None
        self.y_dot_2 = None

    def drag(self, dot_1):
        return (self.rho * (dot_1 ** 2)) / 2

    @property
    def representation(self):
        return "x: {}, y: {}".format(self.x_dot_2, self.y_dot_2)

    def act(self, pc):
        self.x_dot_2 = self.drag(pc.x_dot_1_array) / pc.mass_array
        self.y_dot_2 = self.drag(pc.y_dot_1_array) / pc.mass_array

        x_sign = -1 * pc.x_dot_1_sign_array
        y_sign = -1 * pc.y_dot_1_sign_array

        pc.x_dot_2_array = pc.x_dot_2_array + (self.x_dot_2 * x_sign)
        pc.y_dot_2_array = pc.y_dot_2_array + (self.y_dot_2 * y_sign)


class ControlForce(Force):

    def __init__(self, x_value, y_value):
        super(ControlForce, self).__init__()
        self.x_value = x_value
        self.y_value = y_value

    def act(self, pc):
        pc.x_dot_2_array += self.item_array * (self.x_value / pc.mass_array)
        pc.y_dot_2_array += self.item_array * (self.y_value / pc.mass_array)


class BrakeForce(Force):
    """
    Acts against the current motion of objects with a constant value

    The same deceleration value is applied to both x and y axis
    """

    def __init__(self, value, truncate_multiplier: int = 3, *args, **kwargs):
        kwargs['name'] = 'brake_force'
        super(BrakeForce, self).__init__(*args, **kwargs)
        self.value = value
        self.truncate_multiplier = truncate_multiplier

    def act(self, pc: PhysicsController):
        x_sign = - pc.x_dot_1_sign_array
        y_sign = - pc.y_dot_1_sign_array

        stopped_x_array = abs(
            pc.x_dot_1_array) < self.truncate_multiplier * pc.truncate_value
        stopped_y_array = abs(
            pc.y_dot_1_array) < self.truncate_multiplier * pc.truncate_value

        x_item_array = self.item_array.copy()
        y_item_array = self.item_array.copy()

        x_item_array[stopped_x_array] = 0
        y_item_array[stopped_y_array] = 0

        pc.x_dot_1_array[x_item_array < 0.1] = 0
        pc.y_dot_1_array[y_item_array < 0.1] = 0

        acceleration = self.value / pc.mass_array

        pc.x_dot_2_array += x_item_array * (x_sign * acceleration)
        pc.y_dot_2_array += y_item_array * (y_sign * acceleration)
