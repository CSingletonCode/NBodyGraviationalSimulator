import pygame as pg
from ui.element import Element

class Button(Element):
    def __init__(self, position, size, purpose, colour, border_colour, label, corner_radius, border_size):
        super().__init__(position, size, colour, border_colour, corner_radius, border_size)
        self.purpose = purpose
        self.label = label

        self.pressed = False

    def update(self, mouse_position):
        if not self.enabled:
            self.hovered = False
            return

        self.hovered = self.rect.collidepoint(mouse_position)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.pressed = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed and self.hovered:
                self.purpose()
                self.pressed = False