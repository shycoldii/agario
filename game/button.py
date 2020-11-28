from vector import vector
from game.map import Map
from display import Display

class Button:
    def __init__(self, pos, size, text, on_click = None, display= None, ini= None):
        self.pos = pos
        self.size = size
        self.on_click = on_click
        self.when_display = display
        self.text = text
        ini(self)

    def is_mouse_near(self, mouse_pos):
        """Находится ли мышь над этой кнопкой?
        """
        res = False
        if mouse_pos.x > self.pos.x and mouse_pos.x < self.pos.x + self.size.x:
            if mouse_pos.y > self.pos.y and mouse_pos.y < self.pos.y + self.size.y:
                res = True
        return res

    def display(self, mouse_pos):
        """Отобразить кнопки"""
        return self.when_display(self, mouse_pos)

def button_init(button):
    """Инициализация кнопки старт"""
    button.color_hue = 0
    button.color_sat = 100

def button_start(button, mouse_pos):
    """Отображение кнопки пуск"""
    if button.is_mouse_near(mouse_pos):
        hand_cursor = True
    else:
        hand_cursor = False
    min_size = max(button.size.x, button.size.y)
    font_size = min_size*50/400
    Display.draw_text(button.text,
                      button.pos + button.size / 2,
                      color=(0, 0, 0),
                      size=font_size)
    return hand_cursor

def button_win_end(button, first_try, color):
    """Инициализации кнопки завершения"""
    button.color = color
    if first_try:
        button.alpha = 0

def button_end(button, mouse_pos):
    """Конечный текст"""
    min_size = max(button.size.x, button.size.y)
    font_size = min_size*50/400
    Display.draw_rect(vector(0, 0), Display.size, (0, 0, 0, button.alpha))
    if button.alpha < 127:
        button.alpha += 1
    elif button.alpha < 255 and Map.end:
        button.alpha += 1
    Display.draw_text(button.text,
                      button.pos + button.size / 2,
                      color=button.color,
                      size=font_size)

def button_end_choice(button, mouse_pos):
    """Отображении кнопки конца"""
    min_size = max(button.size.x, button.size.y)
    font_size = min_size*50/400
    if button.is_mouse_near(mouse_pos):
        hand_cursor = True
        c = (0, 0, 0)
        f = True
    else:
        hand_cursor = False
        c = button.color
        f = False
    if "Еще игру?" in button.text:
        Display.draw_rect(button.pos,
                          button.size,
                          color=(0, 255, 0),
                          fill=f)
    else:
        Display.draw_rect(button.pos,
                          button.size,
                          color=(255, 0, 0),
                          fill=f)
    Display.draw_text(button.text,
                      button.pos + button.size / 2,
                      color=c,
                      size=font_size)
    return hand_cursor

def button_win(button, mouse_pos):
    """Кнопка победы"""
    min_size = max(button.size.x, button.size.y)
    font_size = min_size*50/400
    Display.draw_rect(vector(0, 0), Display.size, (0, 0, 0, button.alpha))
    if button.alpha < 127:
        button.alpha += 1
    elif button.alpha < 255 and Map.end:
        button.alpha += 1
    score = Map.info.get("score", 0)
    tps = Map.info.get("time", 0)
    Display.draw_text(button.text,
                      button.pos + button.size / 2,
                      color=button.color,
                      size=font_size)
    Display.draw_text("Счёт: " + str(score),
                      button.pos + button.size / 2 + vector(0, button.size.y),
                      color=button.color,
                      size=font_size)
    Display.draw_text("Время: " + str(tps) + " секунд",
                      button.pos + button.size / 2 + vector(0, button.size.y * 2),
                      color=button.color,
                      size=font_size)
