import os

import settings
import time
import random
import math

from vector import vector
from display import Display
from player_view import Viewer
from game.food import Food
from game.player import Player
from game.enemy import Enemy
from game.bush import Bush
from game.creature import Creature
from skins import Skins

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


class Map:
    end = None
    FOOD = None
    all_food = None
    grid = None
    focus = None
    UPDATING_FOOD = None
    ENIMIES = None
    start_time = None
    info = None
    all_usernames = None
    MAX_SPLIT = None
    bushes = None
    size = None
    grid_size = None
    DELTA_FOOD = None
    player_id = None
    creatures = None

    @classmethod
    def init(cls, width, height):
        cls.size = vector(width, height)
        cls.FOOD = settings.FOOD
        cls.UPDATING_FOOD = settings.UPDATINGFOOD
        cls.DELTA_FOOD = settings.DELTA_FOOD
        cls.MAX_SPLIT = settings.MAX_SPLIT
        cls.grid_size = vector(settings.GRID_WIDTH, settings.GRID_HEIGHT)
        cls.ENIMIES = settings.ENIMIES + 1
        Creature.notify = cls.create_from_parent
        try:
            f = open("./data/nicknames.txt", 'r')
            cls.all_usernames = []
            line = f.readline()
            while line != "":
                line = line.replace('\n', '')
                line = line.replace('\r', '')
                cls.all_usernames.append(line)
                line = f.readline()
            f.close()
        except FileNotFoundError:
            print("Не найден файл usernames")
            cls.all_usernames = None
        cls.reset()

    @classmethod
    def reset(cls):
        """Перезагрузка карты"""
        cls.start_time = time.time()
        cls.end = False
        cls.info = {}
        cls.all_food = []
        cls.ref_time = -1 * cls.DELTA_FOOD
        cls.grid = [[[] for y in range(cls.grid_size.y)] for x in range(cls.grid_size.x)]
        cls.creatures = {}
        cls.player_id = cls.get_id()
        cls.focus = cls.player_id
        hue = random.randrange(0, 360)
        player = Player(vector(cls.size.x / 2, cls.size.y / 2),
                        "YOU",
                        ToRGB(hue, 100, 100),
                        cls.player_id,
                        img=Skins.get_player_skin())
        cls.creatures[cls.player_id] = [player]
        cls.bushes = []
        for i in range(settings.BUSHES):
            cls.create_bush()

    @classmethod
    def get_id(cls):
        return random.randrange(10 ** 64)

    @classmethod
    def create_bush(cls):
        ok = False
        timeout = 0
        while not ok and timeout < 1000:
            ok = True
            pos = vector(random.randint(Bush.RADIUS * 2, cls.size.x - Bush.RADIUS * 2),
                         random.randint(Bush.RADIUS * 2, cls.size.x - Bush.RADIUS * 2))
            for bush in cls.bushes:
                if vector.dist(pos, bush.pos) < Bush.RADIUS * 4:
                    ok = False
            timeout += 1
        if ok:
            cls.bushes.append(Bush(pos))

    @classmethod
    def create_from_parent(cls, parent, is_player, override_limit):
        if len(cls.creatures[parent.creature_id]) < cls.MAX_SPLIT or override_limit:
            parent.score //= 2
            parent.inertia = 0.25
            if is_player:
                creature = Player(parent.pos.copy(), parent.name, parent.color, parent.creature_id, parent.img, parent.radius)
            else:
                creature = Enemy(parent.pos.copy(), parent.name, parent.color, parent.creature_id, parent.img, parent.radius)
            creature.family.extend(parent.family)
            parent.family = creature.family
            creature.score = parent.score
            creature.radius = 1
            creature.speed = parent.speed.copy()
            creature.split_speed = 2
            cls.creatures[parent.creature_id].append(creature)

    @classmethod
    def create_enemy(cls):
        ok = False
        timed_out = False
        c = 0
        rad = random.randint(27, 60)
        while not ok and not timed_out:
            ok = True
            pos = vector(random.randrange(rad * 2, cls.size.x - rad * 2),
                         random.randrange(rad * 2, cls.size.y - rad * 2))
            for k in cls.creatures.keys():
                creatures_list = cls.creatures[k]
                for creature in creatures_list:
                    if vector.dist(pos, creature.pos) < (rad + creature.radius) * 2:
                        ok = False
            if c == 10:
                timed_out = True
            c += 1

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if not timed_out:
            hue = random.randrange(0, 360)
            enemy_id = cls.get_id()

            name = cls.all_usernames[random.randrange(len(cls.all_usernames))]
            skin = Skins.get_rand_skin()

            tmp_list = []
            for i in cls.creatures.values():
                tmp_list.append(i[0].name)
            while name in tmp_list:
                name = cls.all_usernames[random.randrange(len(cls.all_usernames))]
            tmp_list = []
            if "pi19" in os.listdir("./data" + "/skins"):
                for i in cls.creatures.values():
                    tmp_list.append(get_key(Skins.all_skins,i[0].img))
                while get_key(Skins.all_skins,skin) in tmp_list:
                    skin = Skins.get_rand_skin()
            enemy = Enemy(pos, name, ToRGB(hue, 100, 100), enemy_id, skin, rad)
            cls.creatures[enemy_id] = [enemy]



    @classmethod
    def set_mouse(cls, mouse_pos):
        for player in cls.creatures[cls.player_id]:
            player.mouse_pos = mouse_pos - vector(Display.size.x / 2, Display.size.y / 2)
            player.mouse_pos += Viewer.pos - player.pos + vector(Display.size.x / 2, Display.size.y / 2)

    @classmethod
    def update_info(cls):
        for k in cls.creatures.keys():
            creatures_list = cls.creatures[k]
            if k == cls.player_id:
                score_player = 0
                for creature in creatures_list:
                    score_player += creature.score
                cls.info["score"] = score_player
                cls.info["time"] = int(1000 * (time.time() - cls.start_time)) / 1000
            for creature in creatures_list:
                if creature.radius * 2 >= min(cls.size.totuple()):
                    cls.end = True

    @classmethod
    def bush_split(cls):
        for k in cls.creatures.keys():
            creatures_list = cls.creatures[k]
            for creature in creatures_list:
                if creature.radius > Bush.RADIUS:
                    for bush in cls.bushes:
                        if vector.dist(bush.pos, creature.pos) < creature.radius:
                            creature.split(is_player=(creature.creature_id == cls.player_id),
                                           override_limit=True)

    @classmethod
    def update_enemy(cls):
        creatures_info = {}
        for k in cls.creatures.keys():
            creatures_list = cls.creatures[k]
            creatures_info[k] = []
            for creature in creatures_list:
                creatures_info[k].append((creature.pos.copy(), creature.radius, creature.score))
        for k in cls.creatures.keys():
            enemy_list = cls.creatures[k]
            if k != cls.player_id:
                for enemy in enemy_list:
                    enemy.set_cell(cls.get_food_pos())
                    other_creatures_infos = []
                    for k2 in creatures_info.keys():
                        if k != k2:
                            for elem in creatures_info[k2]:
                                other_creatures_infos.append(elem)
                    enemy.set_info(other_creatures_infos)
                    enemy.update(cls.size)

    @classmethod
    def update(cls):
        if len(cls.creatures) < cls.ENIMIES:
            cls.create_enemy()
        for bush in cls.bushes:
            bush.update()
        cls.bush_split()
        Creature.map_size = Map.size
        if cls.is_player_alive():
            for player in cls.creatures[cls.player_id]:
                player.update(cls.size)
        cls.update_enemy()
        cls.update_info()
        for k in cls.creatures.keys():
            creatures_list = cls.creatures[k]
            for creature in creatures_list:
                cls.detect_food(creature)
        cls.detect_enemy()
        cls.delete_garbage()
        for i in range(cls.UPDATING_FOOD):
            cls.create_food()

    @classmethod
    def delete_garbage(cls):
        for i in range(len(cls.bushes)):
            try:
                if not cls.bushes[i].is_alive:
                    del cls.bushes[i]
            except:
                pass
        focused_killer_id = None
        for k in cls.creatures.keys():
            for i in range(len(cls.creatures[k]) - 1, -1, -1):
                if not cls.creatures[k][i].is_alive:
                    if k == cls.focus:
                        focused_killer_id = cls.creatures[k][i].killer_id

                    del cls.creatures[k][i]
        for k in list(cls.creatures.keys()):
            if len(cls.creatures[k]) == 0:
                if k == cls.focus:
                    cls.focus = focused_killer_id

                del cls.creatures[k]

    @classmethod
    def get_focus(cls):
        pos = vector(0, 0)
        for creature in cls.creatures[cls.focus]:
            pos += creature.pos
        pos /= len(cls.creatures[cls.focus])
        return pos

    @classmethod
    def get_focus_radius(cls):
        radius = 0
        for creature in cls.creatures[cls.focus]:
            radius += creature.radius
        radius /= len(cls.creatures[cls.focus])

        return radius

    @classmethod
    def is_player_alive(cls):
        try:
            is_alive = cls.creatures[cls.player_id][0].is_alive
        except KeyError:
            is_alive = False
        return is_alive

    @classmethod
    def detect_enemy(cls):
        for k1 in cls.creatures.keys():
            for k2 in cls.creatures.keys():
                enemy_list_1 = cls.creatures[k1]
                enemy_list_2 = cls.creatures[k2]
                for enemy_1 in enemy_list_1:
                    for enemy_2 in enemy_list_2:
                        if enemy_1 is not enemy_2 and enemy_1.is_alive and enemy_2.is_alive:
                            dist = vector.dist(enemy_1.pos, enemy_2.pos)

                            if k1 == k2:
                                t1 = time.time() - enemy_1.invincibility_family_time
                                t2 = time.time() - enemy_2.invincibility_family_time

                                if t1 > Creature.SPLIT_TIME and t2 > Creature.SPLIT_TIME:
                                    if dist <= max(enemy_1.radius, enemy_2.radius):
                                        enemy_1.kill(enemy_2.score)
                                        enemy_2.killed(k1)
                                        family_tmp = []
                                        for creature in enemy_1.family:
                                            if creature is not enemy_2:
                                                family_tmp.append(creature)

                                        enemy_1.family = family_tmp
                            else:
                                if Creature.can_eat(enemy_1.radius, enemy_2.radius):
                                    if dist <= max(enemy_1.radius, enemy_2.radius):
                                        enemy_1.kill(enemy_2.score)
                                        enemy_2.killed(k1)

    @classmethod
    def get_food_pos(cls):
        res = [[None for i in range(cls.grid_size.y)] for j in range(cls.grid_size.x)]
        for x in range(cls.grid_size.x):
            for y in range(cls.grid_size.y):
                content = []
                for cell in cls.grid[x][y]:
                    content.append(cell.pos.copy())
                res[x][y] = tuple(content)
        return res

    @classmethod
    def create_food(cls):
        if time.time() - cls.ref_time > cls.DELTA_FOOD:
            cls.ref_time = time.time()
            x = random.randrange(Food.BASE_RADIUS, cls.size.x - Food.BASE_RADIUS)
            y = random.randrange(Food.BASE_RADIUS, cls.size.y - Food.BASE_RADIUS)
            cell = Food(vector(x, y))
            ok = True
            for k in cls.creatures.keys():
                enemy_list = cls.creatures[k]
                for enemy in enemy_list:
                    if vector.dist(enemy.pos, cell.pos) < cell.radius + enemy.radius:
                        ok = False
            x = int(cell.pos.x / cls.size.x * cls.grid_size.x)
            y = int(cell.pos.y / cls.size.y * cls.grid_size.y)
            if ok:
                cls.all_food.append(cell)
                cls.grid[x][y].append(cell)
            if len(cls.all_food) >= cls.FOOD:
                cls.delete_food(0)

    @classmethod
    def display(cls):
        info_box = {}
        for i in cls.creatures.values():
            if len(i[0].family) > 1:
                sum_score = 0
                for ent in i[0].family:
                    if ent.is_alive:
                        sum_score += ent.score
                info_box[i[0].name] = sum_score
            else:
                info_box[i[0].name] = i[0].score
        try:
            Display.info_box_score(info_box)
        except:
            pass
        w = cls.size.x
        h = cls.size.y
        for x in range(1, cls.grid_size.x):
            Display.draw_line(vector(x * w / cls.grid_size.x, 0),
                              vector(x * w / cls.grid_size.x, h),
                              color=(170, 170, 170),
                              base_pos=Viewer.pos)
        for y in range(1, cls.grid_size.y):
            Display.draw_line(vector(0, y * h / cls.grid_size.y),
                              vector(w, y * h / cls.grid_size.y),
                              color=(170, 170, 170),
                              base_pos=Viewer.pos)
        Display.draw_line(vector(0, 0), vector(w, 0), color=(170, 102, 102), base_pos=Viewer.pos)
        Display.draw_line(vector(w, 0), vector(w, h), color=(170, 102, 102), base_pos=Viewer.pos)
        Display.draw_line(vector(w, h), vector(0, h), color=(170, 102, 102), base_pos=Viewer.pos)
        Display.draw_line(vector(0, h), vector(0, 0), color=(170, 102, 102), base_pos=Viewer.pos)
        cls.display_food()
        for k in cls.creatures.keys():
            enemy_list = cls.creatures[k]
            if k != cls.player_id:
                for enemy in enemy_list:
                    enemy.display()
        if cls.is_player_alive():
            for player in cls.creatures[cls.player_id]:
                player.display()
        for i in range(len(cls.bushes)):
            cls.bushes[i].display()
        x = Display.size.x / 2
        y = Display.size.y / 2
        r = min(x, y) / 50
        Viewer.set_pos(cls.get_focus())
        r = cls.get_focus_radius()
        r = abs(r)  # радиус игрока
        if r < 80:
            r = r ** 0.1
        elif r < 200:
            r = r ** 0.13
        else:
            r = r ** 0.15
        z = math.exp(-r + 1)
        Display.zoom_changer(z)
        if Display.end:
            Map.end = True

    @classmethod
    def display_food(cls):
        for i in range(len(cls.all_food)):
            cls.all_food[i].display()

    @classmethod
    def split_player(cls):
        if cls.is_player_alive():
            player_list = cls.creatures[cls.player_id]  # информация об игроке
            player_list_tmp = []  # временный лист
            for player in player_list:
                player_list_tmp.append(player)
            for player in player_list_tmp:
                player.split(is_player=True)

    @classmethod
    def detect_food(cls, creature):
        for i in range(len(cls.all_food) - 1, -1, -1):
            cell_i = cls.all_food[i]
            if vector.distant(creature.pos, cell_i.pos) < (creature.radius + cell_i.radius) ** 2:
                creature.score += cell_i.score
                cls.delete_food(i)

    @classmethod
    def delete_food(cls, index):
        cell = cls.all_food[index]
        x = int(cell.pos.x / cls.size.x * cls.grid_size.x)
        y = int(cell.pos.y / cls.size.y * cls.grid_size.y)
        for i in range(len(cls.grid[x][y]) - 1, -1, -1):
            if cell == cls.grid[x][y][i]:
                del cls.grid[x][y][i]
        del cls.all_food[index]
