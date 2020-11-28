import math
import time
import settings
import random

from vector import vector
from player_view import Viewer
from display import Display
from skins import Skins


class Creature():
    """Сущность всех созданий"""
    BASE_RADIUS = 25
    BASE_PERCENT = 1 / 10
    BASE_SCORE = 7
    SPEED_COEFF = settings.SPEED_COEFF
    SPEED_SIZE_POWER = settings.SPEED_POWER
    RADIUS_POWER_SCORE = settings.RADIUS_POWER_SCORE
    SPLIT_TIME = settings.SPLIT_TIME
    ALLOW_SKINS = settings.ALLOW_SKINS

    def __init__(self, pos, name, color, creature_id, img, rad):
        self.family = [self]
        self.invincibility_family_time = time.time()
        self.creature_id = creature_id
        self.killer_id = None
        self.pos = pos.copy()
        self.speed = vector(0, 0)
        self.direction = vector(0, 0)
        self.split_speed = 0
        self.inertia = 0
        self.start_rad = rad
        self.radius = rad
        self.color = color
        self.name = name
        self.img = img
        self.score = rad * 7 / 25
        self.is_alive = True

    def get_pos(self, size, grid_size):
        """Абсолютная позиция в сетке"""
        pos_x = int(self.pos.x / size.x * grid_size.x)
        pos_y = int(self.pos.y / size.y * grid_size.y)
        return vector(pos_x, pos_y)

    def display(self):
        if Creature.ALLOW_SKINS:
            Display.draw_img(img=self.img,
                             pos=self.pos,
                             radius=self.radius,
                             base_pos=Viewer.pos)
        else:
            Display.draw_circle(pos=self.pos,
                                color=self.color,
                                radius=self.radius,
                                base_pos=Viewer.pos,
                                purp=True)

        Display.draw_text(text=self.name,
                          size=self.radius * 0.5,
                          color=(0, 0, 0),
                          pos=self.pos,
                          base_pos=Viewer.pos)

    def apply_speed(self, size):
        self.direction *= self.SPEED_COEFF
        self.direction *= 1 + self.split_speed
        self.direction /= Display.now_frame
        area = 2 * math.pi * self.radius ** 2
        self.direction *= area ** (-self.SPEED_SIZE_POWER)
        self.split_speed *= 0.98
        self.inertia *= 0.99
        new_pos = self.pos + self.direction
        # новая позиция
        if new_pos.x > self.radius and new_pos.x < size.x - self.radius:
            self.pos.x = new_pos.x
        if new_pos.y > self.radius and new_pos.y < size.y - self.radius:
            self.pos.y = new_pos.y
        while self.pos.x < self.radius:
            self.pos.x += 1
        while self.pos.x > size.x - self.radius:
            self.pos.x -= 1
        while self.pos.y < self.radius:
            self.pos.y += 1
        while self.pos.y > size.y - self.radius:
            self.pos.y -= 1
        self.radius += (Creature.future_r(self.score, self.start_rad) - self.radius)/10


    @staticmethod
    def can_eat(radius, other_radius):
        area = 2 * math.pi * radius ** 2
        other_area = 2 * math.pi * other_radius ** 2
        return area > other_area * (1 + Creature.BASE_PERCENT)

    @staticmethod
    def future_r(score, start_rar):
        return start_rar + 2 * score ** Creature.RADIUS_POWER_SCORE

    def kill(self, score):
        self.score += score

    def killed(self, killer_id):
        self.killer_id = killer_id
        self.is_alive = False

    @classmethod
    def notify(cls, parent, is_player, override_limit):
        raise NotImplementedError("?")

    def split(self, is_player=False, override_limit=False):
        if self.score > Creature.BASE_SCORE * 3:
            Creature.notify(self, is_player, override_limit)
