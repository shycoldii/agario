"""Ориентация на игрока"""
from vector import vector
from display import Display

class Viewer:
    pos = None
    # Смещение камеры
    center = None
    # Размер центра экрана

    @classmethod
    def init(cls):
        Display.resize_list(cls.change_view)
        cls.pos = vector(0, 0)
        cls.center = vector(0, 0)

    @classmethod
    def set_pos(cls, pos):
        """Обновление обзора"""
        new_pos = pos - cls.center / Display.zoom_factor
        cls.pos += (new_pos - cls.pos) / 10

    @classmethod
    def change_view(cls, width, height):
        cls.center = vector(width, height) / 2