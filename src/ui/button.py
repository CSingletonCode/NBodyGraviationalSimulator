import pygame as pg
from ui.element import Element

class Button(Element):
    def __init__(self, location, dimensions, purpose, colour, border_colour, label, corner_radius):
        super().__init__(location, dimensions, colour, border_colour, corner_radius)
        self.purpose = purpose
        self.label = label

    def button_pressed(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.pressed = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed and self.hovered:
                self.purpose()
                self.pressed = False