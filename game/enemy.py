import math
import random
import time

from settings import WINDOW_HEIGHT
from vector import vector
from game.creature import Creature
from display import Display


class Enemy(Creature):
    """Враг"""

    def __init__(self, pos, name, color, creature_id, img, rad):
        super().__init__(pos, name, color, creature_id, img, rad)
        self.map_cell = None
        self.creatures_info = None
        self.speed = vector(random.random() * 2 - 1, random.random() * 2 - 1)
        self.test_score = 7
        self.checkpoint = time.time()

    def set_cell(self, map_cell):
        self.map_cell = map_cell

    def set_info(self, creatures_info):
        self.creatures_info = creatures_info

    def searching_cells(self, radius, map_size):
        maxi = 0
        pos_maxi = []
        score = 0
        grid_size = vector(len(self.map_cell), len(self.map_cell[0]))
        map_pos = self.get_pos(map_size, grid_size)
        for x in range(map_pos.x - radius, map_pos.x + radius + 1):
            for y in range(map_pos.y - radius, map_pos.y + radius + 1):
                if x in range(grid_size.x) and y in range(grid_size.y):
                    cell = len(self.map_cell[x][y])
                    if cell == maxi:
                        pos_maxi += [(x, y)]
                    elif cell > maxi:
                        maxi = cell
                        pos_maxi = [(x, y)]
        distance_mini = float("inf")
        coords_mini = None
        for x, y in pos_maxi:
            for j in range(len(self.map_cell[x][y])):
                pos = self.map_cell[x][y][j]
                dist = vector.dist(pos, self.pos)
                if dist < distance_mini:
                    score = len(self.map_cell[x][y])
                    distance_mini = dist
                    coords_mini = self.map_cell[x][y][j]
        return coords_mini, score

    def update(self, map_size):
        grid_size = vector(len(self.map_cell), len(self.map_cell[0]))
        max_radius = grid_size.x
        radius = 1
        speed_cell = None
        while speed_cell is None and radius < max_radius:
            speed_cell, cell_score = self.searching_cells(radius, map_size)
            radius += 1
        if speed_cell is None:
            speed_cell = vector(0, 0)
        else:
            speed_cell = speed_cell - self.pos
        speed_target, target, speed_hunter, hunter, can_split = self.speed_enemy(map_size)

        borders = [vector(self.pos.x, self.radius),
                   vector(self.pos.x, map_size.y - self.radius),
                   vector(self.radius, self.pos.y),
                   vector(map_size.x - self.radius, self.pos.y)]
        c_borders = []
        for bord in borders:
            dist_bord = vector.dist(bord, self.pos)
            c_bord = math.exp(-(dist_bord ** 0.2) / 2) ** 3
            c_bord = c_bord if c_bord <= 1 else 0
            c_borders.append(c_bord)
        speed_family = vector(0, 0)
        c_family = 0
        lame = 0
        for creature in self.family:
            if self is not creature:
                lame += 1
                coeff = (time.time() - creature.invincibility_family_time) / self.SPLIT_TIME
                if coeff > 1:
                    coeff = 1
                coeff = coeff ** 3
                c_family += coeff
                speed_family += (creature.pos - self.pos) * coeff
        self.speed *= 0.98 + self.inertia
        if lame != 0:
            c_family /= lame
        direction = (speed_cell * (1 - target) * (1 - hunter) * (1 - c_family)).normalize() \
                    + (speed_target * target * (1 - hunter) * (1 - c_family)).normalize() \
                    - (speed_hunter * (1 - target) * hunter * (1 - c_family)).normalize() \
                    + (speed_family * target * (1 - hunter) * c_family).normalize()
        if can_split:
            if self.speed != vector(0, 0) and speed_target != vector(0, 0):
                angle = vector.get_angle(self.speed, speed_target)
                if abs(angle) < 10:
                    self.split()
        self.speed += direction
        self.speed.x -= 1 * c_borders[0] * self.speed.y
        self.speed.y += 1 * c_borders[0] * abs(self.speed.y)

        self.speed.x -= 1 * c_borders[1] * self.speed.y
        self.speed.y -= 1 * c_borders[1] * abs(self.speed.y)

        self.speed.y += 1 * c_borders[2] * self.speed.x
        self.speed.x += 1 * c_borders[2] * abs(self.speed.x)

        self.speed.y += 1 * c_borders[3] * self.speed.x
        self.speed.x -= 1 * c_borders[3] * abs(self.speed.x)

        self.direction = self.speed.normalize()

        self.apply_speed(map_size)

        if self.score >= 7000:
            self.score = 7000
        if self.score == self.test_score and self.score > 7:
            if time.time() - self.checkpoint >= 30:
                if self.score // 10 > self.test_score - self.score:
                    self.score -= self.score // 10
                    self.test_score = self.score
                    self.checkpoint = time.time()
                else:
                    self.score = 7
                    self.test_score = self.score
                    self.checkpoint = time.time()
        else:
            self.checkpoint = time.time()
            self.test_score = self.score

    def speed_enemy(self, map_size):
        d_target = float("inf")
        d_hunter = float("inf")
        speed_target = None
        speed_hunter = None
        can_split = False
        score_target = None
        for enemy_pos, enemy_radius, enemy_score in self.creatures_info:
            dist = vector.dist(self.pos, enemy_pos) - self.radius - enemy_radius
            if Creature.can_eat(enemy_score, self.score):
                if dist < d_hunter:
                    speed_hunter = enemy_pos - self.pos
                    d_hunter = dist
            elif Creature.can_eat(self.score, enemy_score):
                if dist < d_target:
                    speed_target = enemy_pos - self.pos
                    d_target = dist
                    score_target = enemy_score
        if score_target is not None:
            if score_target < self.score // 2:
                if d_target > self.radius and d_target < self.radius * 2:
                    can_split = True
        if speed_hunter is None:
            speed_hunter = vector(0, 0)
        if speed_target is None:
            speed_target = vector(0, 0)
        target = 1 - d_target / map_size.length()
        target = abs(target ** 3)
        if target == float("inf"):
            target = 0
        elif target >= 1:
            target = 1
        target = target if target != float("inf") else 0
        hunter = 1 - d_hunter / map_size.length()
        hunter = abs(hunter ** 3)
        if hunter == float("inf"):
            hunter = 0
        elif hunter >= 1:
            hunter = 1
        return speed_target, target, speed_hunter, hunter, can_split
