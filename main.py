import pygame
import settings
from game.map import Map
from game.game import Game
from game.menu import Menu
from display import Display
from player_view import Viewer
from skins import Skins


def initialization():
    """инициализация нужных файлов игры"""
    pygame.init()
    Viewer.init()
    Display.init(width=settings.WINDOW_WIDTH,
                 height=settings.WINDOW_HEIGHT,
                 framerate=settings.FRAMERATE)
    Menu.init()
    Skins.init()
    Map.init(width=settings.MAP_WIDTH,
             height=settings.MAP_HEIGHT)


if __name__ == "__main__":
    initialization()
    game = Game()
    game.run()
    pygame.quit()