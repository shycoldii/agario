import pygame

from game.button import *
from game.state import GameState
from game.map import Map
from display import Display

class Menu:
    can_quit = None
    can_play = None
    first_try = None
    mouse_pos = None
    buttons = None
    state = None

    @classmethod
    def init(cls):
        cls.apply_state(GameState.MENU)
        Display.resize_list(cls.create_buttons)

    @classmethod
    def apply_state(cls, state):
        cls.can_play, cls.can_quit = False, False
        cls.state = state
        cls.create_buttons(Display.size.x, Display.size.y, first_try=True)

    @classmethod
    def play(cls):
        """Для переигры"""
        Display.set_cursor()
        Map.reset()
        cls.can_play = True

    @classmethod
    def create_buttons(cls, width, height, first_try = False):
        cls.buttons = []
        cls.first_try = first_try
        if cls.state == GameState.MENU:
            cls.apply_menu(width, height)
        elif cls.state == GameState.WIN:
            cls.apply_win(width, height)
        else:
            cls.apply_end(width, height)

    @classmethod
    def quit(cls):
        cls.can_quit = True

    @classmethod
    def apply_menu(cls, width, height):
        """Меню-состояние"""
        cls.buttons.append(Button(pos=vector(width / 11, height / 3),
                                  size=vector(width / 1.2, height / 3),
                                  text="Agar.io",
                                  on_click=cls.play,
                                  display=button_start,
                                  ini=button_init))
        cls.buttons.append(Button(pos=vector(width / 1.52, height / 1.13),
                                  size=vector(width / 5, height / 5),
                                  text="Разработчики: Александрова Дарья & Брусова Полина",
                                  on_click=cls.play,
                                  display=button_start,
                                  ini=button_init))


    @classmethod
    def apply_end(cls, width, height):
        """Меню конца"""
        cls.buttons.append(Button(pos=vector(width / 4, height / 5),
                                  size=vector(width / 2, height / 5),
                                  text="Поражение!",
                                  display=button_end,
                                  ini=lambda b: button_win_end(b, cls.first_try, (0, 0, 0))))

        cls.buttons.append(Button(pos=vector(width / 5, 3 * height / 5),
                                  size=vector(width / 5, height / 5),
                                  text="Переиграть?",
                                  on_click=cls.play,
                                  display=button_end_choice,
                                  ini=lambda b: button_win_end(b, cls.first_try, (0, 0, 0))))

        cls.buttons.append(Button(pos=vector(3 * width / 5, 3 * height / 5),
                                  size=vector(width / 5, height / 5),
                                  text="Выйти?",
                                  on_click=cls.quit,
                                  display=button_end_choice,
                                  ini=lambda b: button_win_end(b, cls.first_try, (0, 0, 0))))

    @classmethod
    def apply_win(cls, width, height):
        """Меню-победы"""
        cls.buttons.append(Button(pos=vector(width / 4, height / 5),
                                  size=vector(width / 2, height / 10),
                                  text="Победа !",
                                  display=button_win,
                                  ini=lambda b: button_win_end(b, cls.first_try, (0, 0, 0))))

        cls.buttons.append(Button(pos=vector(width / 5, 3 * height / 5),
                                  size=vector(width / 5, height / 5),
                                  text="Еще игру?",
                                  on_click=cls.play,
                                  display=button_end_choice,
                                  ini=lambda b: button_win_end(b, cls.first_try, (0, 0, 0))))

        cls.buttons.append(Button(pos=vector(3 * width / 5, 3 * height / 5),
                                  size=vector(width / 5, height / 5),
                                  text="Выйти?",
                                  on_click=cls.quit,
                                  display=button_end_choice,
                                  ini=lambda b: button_win_end(b, cls.first_try, (0, 0, 0))))

    @classmethod
    def update(cls, mouse_pos, mouse_pressed):
        cls.mouse_pos = mouse_pos
        if mouse_pressed:
            for i in range(len(cls.buttons)):
                if cls.buttons[i].is_mouse_near(cls.mouse_pos):
                    try:
                        cls.buttons[i].on_click()
                    except:
                        pass

    @classmethod
    def display(cls):
        for i in range(len(cls.buttons)):
            cls.buttons[i].display(cls.mouse_pos)
        Display.set_cursor()
