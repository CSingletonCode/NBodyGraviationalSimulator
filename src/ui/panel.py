from ui.element import Element
import pygame as pg


class Panel(Element):
    def __init__(self, position, size, colour, border_colour, corner_radius, border_size, label=None, label_colour=(1,1,1), enable_shadow=False):
        super().__init__(position, size, colour, border_colour, corner_radius, border_size, enable_shadow)
        self.label = label
        self.text_texture = None
        self.font = pg.font.SysFont("Arial", 20, bold=True)
        self.label_colour = label_colour
        self.pressed = False
        self.contains = []

    def add_element(self, element):
        self.contains.append(element)

    def hide(self):
        self.disable()
        for element in self.contains:
            element.disable()

    def show(self):
        self.enable()
        for element in self.contains:
            element.enable()

    def update(self, mouse_position):
        for element in self.contains:
            element.update(mouse_position)

    # def handle_event(self, event):
    #     # for element in self.contains:
    #     #     element.handle_event(event)
    #     pass

    def draw(self, renderer):
        renderer.draw_basics(self)
        renderer.draw_text(self)
        for element in self.contains:
            element.draw(renderer)

