import math

from vector import vector
from display import Display
from player_view import Viewer

class Bush:
    """кусты"""
    RADIUS = 50
    SPEED = 1/900
    SHARPNESS = 0.1
    BASE_HEALTH = 19

    def __init__(self, pos):
        self.pos = pos
        self.angle = 0
        self.health = Bush.BASE_HEALTH

    def update(self):
        self.angle += Bush.SPEED

    def display(self):
        """отображение куста"""
        c = (127, 255, 0)
        for i in range(self.health):
            angle = i/self.health*2*math.pi + self.angle
            offset = vector(math.cos(angle), math.sin(angle)) * Bush.RADIUS * (1 + Bush.SHARPNESS / 3)
            Display.draw_triangle(pos=self.pos + offset,
                                  color=c,
                                  radius=Bush.RADIUS*Bush.SHARPNESS,
                                  angle=2*math.pi/self.health*i + self.angle,
                                  base_pos=Viewer.pos)

        Display.draw_circle(pos=self.pos,
                            color=c,
                            radius=Bush.RADIUS,
                            base_pos=Viewer.pos)
