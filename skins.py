import pygame
import pygame.gfxdraw
import os
import random

from vector import vector

default_skin = "skin1"

class Skins:
    all_skins = None
    PATH = "./data"
    @classmethod
    def init(cls):
        cls.all_skins = {}
        all_skins = cls.loadskins() #грузим все скины из папки
        for name in all_skins.keys():
            img = all_skins[name]
            circle = cls.Image_to_circle(img)
            cls.all_skins[name] = (circle)

    @classmethod
    def loadskins(cls):
        """Загрузка скинов из папки"""
        all_img = {}
        flag = 0
        full_names = os.listdir(cls.PATH + "/skins")
        if "pi19" in full_names:
            full_names = os.listdir(cls.PATH + "/skins/pi19")
            flag = 1
        for file in full_names:
            file_name = file.split('.')
            if True:
                extension = file_name[-1] #расширение
                del file_name[-1]
                file_name = ''.join(file_name)
                if extension in ("png", "jpg"):
                    if flag:
                        img = pygame.image.load(cls.PATH + "/skins/pi19/" + file_name + '.' + extension).convert()
                    else:
                        img = pygame.image.load(cls.PATH + "/skins/" + file_name + '.' +extension).convert()
                    all_img[file_name] = (img)
        return all_img

    @classmethod
    def get_player_skin(cls):

        #player_skin = pygame.image.load(cls.PATH + "/skins/skin1.png").convert()
        #circle = cls.Image_to_circle(player_skin)
        player_skin = []
        if "pi19" in os.listdir(cls.PATH + "/skins"):
            player_skin.append("g5")
            player_skin.append("g7")
            return cls.all_skins[random.choice(player_skin)]
        else:
            return cls.all_skins[list(cls.all_skins.keys())[random.randrange(len(list(cls.all_skins.keys())))]]

    @classmethod
    def get_rand_skin(cls):
        skin = list(cls.all_skins.keys())[random.randrange(len(list(cls.all_skins.keys())))]
        return cls.all_skins[skin]

    @classmethod
    def Image_to_circle(cls, img):
        """Конвертирует картинку в круг"""
        width = img.get_width()
        height = img.get_height()
        if width == height:
            size = width
        else:
            raise ValueError("Одна из картинок имеет неквадратный формат")

        surface = pygame.Surface((size+1, size+1), pygame.SRCALPHA)
        center = vector(size / 2, size / 2)
        radius = int(size/2)

        for x in range(size):
            for y in range(size):
                pos = vector(x, y)
                if vector.distant(pos, center) < radius**2:
                    color = img.get_at((x, y))
                    if color[3] != 255:
                        color[3] = 255
                        #если есть прозрачность
                    if color == (99, 28, 11):
                        color[0] += 1
                else:
                    color = (255, 255, 255, 0)
                    # Вне круга будет прозрачный цвет
                pygame.gfxdraw.pixel(surface, x, y, color)

        pygame.gfxdraw.aacircle(surface, int(size/2), int(size/2), radius, (0, 0, 0))
        surface.set_colorkey((99, 28, 11))
        surface = surface.convert_alpha()
        return surface



