import time
import math
import pygame
import pygame.gfxdraw

from vector import vector

class Display:
    resized_list = []
    user_size = None
    size = None
    window_size = None
    is_fullscreen= False
    zoom_factor = 1
    framerate = None
    now_frame = None
    frame_count = 0
    last_frame = time.time()
    frametimes = [0 for i in range(10)]
    clock = pygame.time.Clock()
    all_font = {}
    window = None
    end = False

    @classmethod
    def init(cls, width, height, framerate):
        cls.set_cursor()
        cls.user_size = vector(pygame.display.Info().current_w,  #размер экрана "компьютера"
                               pygame.display.Info().current_h)
        cls.size = vector(width, height) #заданные настройки
        cls.window_size = cls.size.copy()
        #Размер окна будет такой, как текущий
        cls.framerate = framerate
        cls.now_frame = cls.framerate
        cls.resize(cls.size.x, cls.size.y)
        # Создание окна с заданными настройками
        cls.update_frame()

    @staticmethod
    def set_cursor():
        """Курсор вида треугольник"""
        try:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        except:
            pass

    @classmethod
    def info_box_score(cls, info):
        cls.draw_rect(vector(cls.window_size.x//1.25,cls.window_size.y//600),vector(cls.window_size.x//5,cls.window_size.y//2.75),(125,125,125))
        r=(cls.window_size.y//2.75)/20
        flag = 0
        place = 0
        sorted_x = sorted(info.items(), key=lambda kv: kv[1], reverse=True)
        sorted_10 = sorted_x[0:10]
        if sorted_10[0][0] == 'YOU':
            Display.end = True

        for i in sorted_10:
            if i[0] == 'YOU':
                flag = 1
                break

        if not flag:
            for i in sorted_x:
                if i[0] == "YOU":
                      place = sorted_x.index(i)+1
                      break
        c = 1

        for i in sorted_10:
            if i[0] == "YOU":
                cls.draw_text(f"{c}. {i[0]}: {int(i[1])}",vector(cls.window_size.x//1.12,cls.window_size.y//600+r),color=(255,0,0),size=cls.window_size.x//40)
            else:
                cls.draw_text(f"{c}. {i[0]}: {int(i[1])}",
                              vector(cls.window_size.x // 1.12, cls.window_size.y // 600 + r),size=cls.window_size.x//40)
            r += (cls.window_size.y//2.75)/11

            c+=1

        if not flag:
            cls.draw_text(f"{place}. {'YOU'}: {int(info['YOU'])}", vector(cls.window_size.x // 1.12, cls.window_size.y // 600 + r),color = (255,0,0),size=cls.window_size.x//40)


    @classmethod
    def full_screen(cls):
        """Изменение полного экрана при F12"""
        cls.is_fullscreen = not cls.is_fullscreen
        if cls.is_fullscreen:
            cls.resize(cls.user_size.x, cls.user_size.y)
            # на размер полного "компьютерного" экрана
        else:
            cls.resize(cls.window_size.x, cls.window_size.y)
            # на определенный размер

    @classmethod
    def resize(cls, w, h):
        """Изменение размера экрана"""
        if cls.is_fullscreen:
            cls.window = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
        else:
            cls.window = pygame.display.set_mode((w, h), pygame.RESIZABLE)
            cls.window_size = vector(w, h)
        cls.size = vector(w, h)
        for func in cls.resized_list:
            func(w, h)

    @classmethod
    def resize_list(cls, f):
        cls.resized_list.append(f)

    @classmethod
    def updateTitle(cls):
        """Заголовок окна изменения"""
        pygame.display.set_caption("Agar.io - " + str(cls.now_frame) + " fps")

    @classmethod
    def update_frame(cls, color=(230, 235, 235)):
        """Обновление окна"""
        pygame.display.flip()
        if len(color) == 3:
            cls.window.fill(color)
            #фон
        else:
            cls.draw_rect(vector(0, 0), cls.size, color)
        cls.updateTitle()
        #===процедура обновления фпс
        del cls.frametimes[0]
        cls.frametimes.append(time.time() - cls.last_frame)
        frametime = sum(cls.frametimes)/len(cls.frametimes)
        if frametime == 0:
            cls.now_frame = float("inf")
        else:
            cls.now_frame = round(1 / frametime)
        cls.last_frame = time.time()
        cls.clock.tick(cls.framerate)
        cls.frame_count += 1

    @classmethod
    def zoom_changer(cls, zoom):
        """Масштабирование"""
        if zoom == 0:
            raise ValueError("Zoom нулевой")
        elif zoom < 0:
            raise ValueError("Zoom отрицательный")
        cls.zoom_factor += (zoom - cls.zoom_factor) / 10

    @classmethod
    def draw_circle(cls, pos, color, radius, base_pos=vector(0, 0), fill=True, purp = None):
        """Рисует круг на экране"""
        pos = pos.copy()
        if base_pos.length() != 0:
            pos = (pos - base_pos)*cls.zoom_factor
        pos = pos.toint()
        radius = int(radius*cls.zoom_factor)
        if pos.x in range(-radius, cls.size.x+radius) and pos.y in range(-radius, cls.size.y+radius):
            if fill: #полный круг
                pygame.draw.circle(cls.window, color, (pos.x, pos.y), radius)

            if purp:
                color = [col/2 for col in list(color)]
                color = tuple(color)
                pygame.draw.circle(cls.window, color, (pos.x, pos.y), radius, width=5)

    @classmethod
    def draw_rect(cls, pos, size, color, base_pos=vector(0, 0), fill=True):
        """Рисует прямугоугольник"""
        size = size.copy()
        pos = pos.copy()
        if base_pos.length() != 0:
            pos = (pos - base_pos)*cls.zoom_factor
        pos = pos.toint()
        if base_pos.length() != 0:
            size *= cls.zoom_factor
        size = size.toint()
        rect = pygame.Rect(pos.totuple(), size.totuple())
        if fill:
            pygame.gfxdraw.box(cls.window, rect, color)
        else:
            pygame.gfxdraw.rectangle(cls.window, rect, color)

    @classmethod
    def draw_text(cls, text, pos, size=16, color=(255, 255, 255), base_pos=vector(0, 0)):
        pos = pos.copy()
        if base_pos.length() != 0:
            pos = (pos - base_pos)*cls.zoom_factor
        pos = pos.toint()
        if base_pos.length() != 0:
            size *= cls.zoom_factor
        font_size = round(size)  # надо тут как-то поменять размер шрифта
        if not (pos.x in range(-font_size*len(text), cls.size.x+font_size*len(text)) and pos.y in range(-font_size, cls.size.y+font_size)):
            return
        font_family = "Roboto-Black.tff"
        if cls.all_font.get(font_family, None) is None:
            cls.all_font[font_family] = {}
        if cls.all_font[font_family].get(size, None) is None:
            cls.all_font[font_family][font_size] = pygame.font.SysFont(font_family, font_size)
        font = cls.all_font[font_family][font_size]
        text = str(text)
        color = [int(color[i]) if color[i] <= 255 else 255 for i in range(len(color))]
        text_surface = font.render(text, True, color)
        if len(color) == 4 and color[3] != 255:
            # если есть прозрачность
            alpha_img = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            alpha_img.fill((255, 255, 255, color[3]))
            text_surface.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        size = vector(text_surface.get_width(), text_surface.get_height())
        pos -= size//2
        cls.window.blit(text_surface, pos.totuple())

    @classmethod
    def draw_line(cls, pos1, pos2, color, base_pos=vector(0, 0), width=1):
        pos1 = pos1.copy()
        pos2 = pos2.copy()
        if base_pos.length() != 0:
            pos1 = (pos1 - base_pos)*cls.zoom_factor
            pos2 = (pos2 - base_pos)*cls.zoom_factor
        pos1 = pos1.toint()
        pos2 = pos2.toint()
        if width == 1:
            pygame.gfxdraw.line(cls.window, pos1.x, pos1.y, pos2.x, pos2.y, color)
        else:
            pygame.draw.line(cls.window, color, pos1.totuple(), pos2.totuple(), width)

    @classmethod
    def draw_triangle(cls, pos, color, radius, angle, base_pos=vector(0, 0), fill=True):
        pos = pos.copy()
        if base_pos.length() != 0:
            pos = (pos - base_pos)*cls.zoom_factor
        pos = pos.toint()
        nodes = []
        for i in range(3):
            local_angle = 2*i*math.pi/3 + angle
            nodes.append(int(pos.x + math.cos(local_angle)*radius*cls.zoom_factor))
            nodes.append(int(pos.y + math.sin(local_angle)*radius*cls.zoom_factor))
        if fill:
            pygame.gfxdraw.filled_trigon(cls.window, *nodes, color)
        pygame.gfxdraw.aatrigon(cls.window, *nodes, color)

    @classmethod
    def draw_img(cls, img, pos, base_pos=vector(0, 0), radius=None):
        pos = pos.copy()
        if base_pos.length() != 0:
            pos = (pos - base_pos)*cls.zoom_factor
        pos = pos.toint()
        radius = int(radius*cls.zoom_factor)
        if radius is not None:
            pos -= vector(radius, radius)
            img = pygame.transform.smoothscale(img, (radius*2, radius*2))
        cls.window.blit(img, pos.totuple())

    @classmethod
    def draw_start_img(cls,img,pos):
        cls.window.blit(pygame.transform.smoothscale(img,(50,50)), pos.totuple())

    @classmethod
    def fon(cls,img):
        cls.window.blit(img,(0,0))