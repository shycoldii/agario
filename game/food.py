import random

from display import Display
from player_view import Viewer


def ToRGB(h, s, v, a=255):

    while h < 0:
        h += 360 * 100
    h %= 360
    h /= 360

    while s < 0:
        s += 101 * 100
    s %= 101
    s /= 100

    while v < 0:
        v += 101 * 100
    v %= 101
    v /= 100

    # Pour avoir des valeurs entre 0 et 1

    if s == 0:
        r = g = b = int(v * 255)
    else:
        i = int(h * 6)
        f = (h * 6) - i
        p = int(255 * v * (1 - s))
        q = int(255 * v * (1 - s * f))
        t = int(255 * v * (1 - s * (1 - f)))

        v = int(v * 255)

        i %= 6

        if i == 0:
            r, g, b = (v, t, p)
        elif i == 1:
            r, g, b = (q, v, p)
        elif i == 2:
            r, g, b = (p, v, t)
        elif i == 3:
            r, g, b = (p, q, v)
        elif i == 4:
            r, g, b = (t, p, v)
        elif i == 5:
            r, g, b = (v, p, q)

    return (r, g, b, a)

class Food:
    """Еда"""
    BASE_RADIUS = 8
    def __init__(self, pos):
        hue = random.randrange(0, 360)
        self.color = ToRGB(hue, 100, 100)
        self.pos = pos
        self.radius = self.BASE_RADIUS
        self.score = 1
    def display(self):
        """Отображение"""
        Display.draw_circle(pos=self.pos,
                            color=self.color,
                            radius=self.radius,
                            base_pos=Viewer.pos)
