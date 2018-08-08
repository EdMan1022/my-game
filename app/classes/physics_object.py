import pyxel


class PhysicsObject(object):
    __slots__ = ('x_i', 'x_dot_1_i', 'y_i', 'y_dot_1_i', 'mass',
                 'physics_controller', 'index')

    def __init__(self, x_i: float, x_dot_1_i: float,
                 y_i: float, y_dot_1_i: float, mass: float,
                 physics_controller=None):
        self.x_i = x_i
        self.x_dot_1_i = x_dot_1_i
        self.y_i = y_i
        self.y_dot_1_i = y_dot_1_i
        self.mass = mass
        self.index = None

        self.physics_controller = physics_controller

    def __repr__(self):
        return ("(x: {:03.2f}, x_dot: {:03.2f}, x_dot_2: {:03.2f}),"
                "\n(y: {:03.2f}, y_dot: {:03.2f}, y_dot_2: {:03.2f})").format(
            self.x, self.x_dot_1, self.x_dot_2, self.y, self.y_dot_1,
            self.y_dot_2
        )

    @property
    def x(self):
        return self.physics_controller.x_array[self.index]

    @property
    def x_dot_1(self):
        return self.physics_controller.x_dot_1_array[self.index]

    @property
    def x_dot_2(self):
        return self.physics_controller.prev_x_dot_2_array[self.index]

    @property
    def y(self):
        return self.physics_controller.y_array[self.index]

    @property
    def y_dot_1(self):
        return self.physics_controller.y_dot_1_array[self.index]

    @property
    def y_dot_2(self):
        return self.physics_controller.prev_y_dot_2_array[self.index]

    def draw(self, app):
        pyxel.pix(x=self.x % app.width, y=self.y % app.height, col=7)


class PhysicsBox(PhysicsObject):
    __slots__ = ('width', 'height', 'col', '__dict__')

    def __init__(self, width=6, height=8, col=9, *args, **kwargs):
        super(PhysicsBox, self).__init__(*args, **kwargs)

        self.width = width
        self.height = height
        self.col = col

    def draw(self, app):
        normalized_x = self.x % app.width
        normalized_y = self.y % app.height

        pyxel.rect(
            x1=normalized_x,
            y1=normalized_y,
            x2=normalized_x + self.width,
            y2=normalized_y + self.height,
            col=self.col
        )
