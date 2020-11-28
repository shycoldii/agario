from vector import vector
from game.creature import Creature
from display import Display
import time

class Player(Creature):
    """Игрок"""
    mouse_pos = vector()

    def __init__(self, pos, name, color, creature_id, img, rad=25):
        super().__init__(pos, name, color, creature_id, img, rad)
        self.test_score = 7
        self.checkpoint = time.time()



    def update(self, map_size):
        if self.mouse_pos.sq_norm() > self.radius**2:
            coef_dist = 1
        else:
            coef_dist = self.mouse_pos.length()/self.radius
            coef_dist = coef_dist**2
        self.speed = self.mouse_pos.normalize()*coef_dist + self.speed*0.95
        self.direction = self.speed.normalize()*coef_dist
        self.apply_speed(map_size)
        if self.score >= 7000:
            self.score = 7000
        if self.score == self.test_score and self.score > 7:
            if time.time() - self.checkpoint >= 30:
                if self.score//10 > self.test_score - self.score:
                    self.score -= self.score//10
                    self.test_score = self.score
                    self.checkpoint = time.time()
                else:
                    self.score = 7
                    self.test_score = self.score
                    self.checkpoint = time.time()
        else:
            self.checkpoint = time.time()
            self.test_score = self.score

