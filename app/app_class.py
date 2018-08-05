import math

import pyxel


class App(object):

    __slots__ = ('width', 'height', 'x',
                 '_x_update', '_x_speed', 'y', '_y_update', 'y_speed',
                 'key_up', 'key_down', 'key_left', 'key_right',
                 '__dict__')

    def __init__(self, width: int=160, height: int=120):

        self.width = width
        self.height = height

        self.box_width = 9
        self.box_height = 9
        self.box_color = 7

        self.x = 0
        self.y = self.height / 2

        self.x2 = self.x + self.box_width
        self.y2 = self.y + self.box_height

        self.x_speed = 1
        self.x_slow = .2
        self.y_speed = 1
        self.y_slow = .5
        self._x_update = 0
        self._y_update = 0
        self._init_pyxel()

        self.key_up = pyxel.constants.KEY_W
        self.key_down = pyxel.constants.KEY_S
        self.key_left = pyxel.constants.KEY_A
        self.key_right = pyxel.constants.KEY_D

    def _init_pyxel(self):
        pyxel.init(self.width, self.height, fps=60)

    def _parse_x_input(self):
        if pyxel.btn(self.key_left):
            self._x_update -= self.x_speed

        if pyxel.btn(self.key_right):
            self._x_update += self.x_speed

    def _parse_y_input(self):
        if pyxel.btn(self.key_up):
            self._y_update -= self.y_speed

        if pyxel.btn(self.key_down):
            self._y_update += self.y_speed

    def _parse_key_input(self):
        self._parse_x_input()
        self._parse_y_input()

    def _apply_x_input(self):

        self.x = (self.x + self._x_update) % self.width
        self.x2 = self.x + self.box_width

    def _apply_y_input(self):

        self.y = (self.y + self._y_update) % self.height
        self.y2 = self.y + self.box_height

    def _apply_key_input(self):
        self._apply_x_input()
        self._apply_y_input()

    def _x_updater(self):
        update = abs(self._x_update)
        math.log(update)
        update = max(update - self.x_slow, 0)
        if self._x_update < 0:
            update *= -1
        self._x_update = update

    def _clear_x_updates(self):
        self._x_update = self.clear_updates(self._x_update, self.x_updater)

    @staticmethod
    def clear_updates(update, update_func):
        abs_update = abs(update)
        abs_update = update_func(abs_update)
        if update < 0:
            abs_update *= -1
        return abs_update

    def x_updater(self, update):
        if update > 1:
            update = update ** .5
        return max(update - self.x_slow, 0)

    def y_updater(self, update):
        return max(update - self.y_slow, 0)

    def _clear_y_updates(self):
        self._y_update = self.clear_updates(self._y_update, self.y_updater)

    def _clear_key_updates(self):
        self._clear_x_updates()
        self._clear_y_updates()

    def update(self):

        self._parse_key_input()
        self._apply_key_input()
        self._clear_key_updates()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(x1=self.x, y1=self.y, x2=self.x2, y2=self.y2,
                   col=self.box_color)

    def run(self):
        pyxel.run(self.update, self.draw)
