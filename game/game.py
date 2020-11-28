import pygame

from vector import vector
from game.map import Map
from game.menu import Menu
from game.state import GameState
from display import Display
from game.player import Player
from settings import WINDOW_WIDTH,WINDOW_HEIGHT

class Game:
    """ Cостояния state
            0 - стратовое меню
            1 - игра
            2 - проигрыш
            3 - победа
            """
    finished = False  # переменная, отвечающая за конец игры
    state = GameState.MENU  # переменная, отвечающая за состояние игры

    @classmethod
    def run(cls):
        """Запуск игры"""
        while not cls.finished:
            cls.handleKeys()
            mx, my = pygame.mouse.get_pos()
            mouse_pos = vector(mx, my)
            mouse_pressed = pygame.mouse.get_pressed()[0]
            Menu.state = GameState.MENU
            if cls.state == GameState.MENU:
                Display.draw_start_img(pygame.image.load("data/game_images/start1.png"), vector(0, 0))
                Display.draw_start_img(pygame.image.load("data/game_images/f12.png"), vector(50, 0))
                Display.draw_start_img(pygame.image.load("data/game_images/esc.png"), vector(0, 50))
                Display.draw_start_img(pygame.image.load("data/game_images/space.png"), vector(50, 50))
                Menu.update(mouse_pos, mouse_pressed)
                if Menu.can_play:
                    cls.state = GameState.GAME
                if Menu.can_quit:
                    cls.finished = True
                Menu.display()
                if Menu.can_play:
                    Display.set_cursor()

            elif cls.state == GameState.END:
                Menu.update(mouse_pos, mouse_pressed)
                if not Map.end:
                    Map.update()
                if Menu.can_play:
                    cls.state = GameState.GAME
                    Display.end = False
                    Map.end = False
                if Menu.can_quit:
                    cls.finished = True
                Map.display()
                Menu.display()
                if Menu.can_play:
                    Display.set_cursor()
            elif cls.state == GameState.WIN:
                Menu.update(mouse_pos, mouse_pressed)
                if Menu.can_play:
                    cls.state = GameState.GAME
                    Display.end = False
                    Map.end = False
                if Menu.can_quit:
                    cls.finished = True
                Menu.display()
                if Menu.can_play:
                    Display.set_cursor()
            elif cls.state == GameState.GAME:
                Map.set_mouse(mouse_pos / Display.zoom_factor)
                Map.update()
                Map.display()
                if Map.is_player_alive():
                    if Map.end:
                        cls.state = GameState.WIN
                        Menu.apply_state(GameState.WIN)
                else:
                    cls.state = GameState.END
                    Menu.apply_state(GameState.END)
            Display.update_frame()


    @classmethod
    def handleKeys(cls):
        """Функция, проверяющая нажатие кнопок клавиатуры"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            cls.finished = True  # выход из игры
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                Display.resize(event.w, event.h)
                # изменение размера экрана
            if event.type == pygame.QUIT:
                cls.finished = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    Display.full_screen()  # полноэкранный размер
                if event.key == pygame.K_SPACE:  # разбиение нашего шарика
                    if Map.is_player_alive():
                        Map.split_player()
