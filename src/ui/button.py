import pygame as pg
from ui.element import Element

class Button(Element):
    def __init__(self, position, size, purpose, colour, border_colour, label, label_colour, corner_radius, border_size, enable_shadow):
        super().__init__(position, size, colour, border_colour, corner_radius, border_size, enable_shadow)
        self.purpose = purpose
        self.label = label
        self.text_texture = None
        self.pressed = False
        self.font = pg.font.SysFont("Arial", 20, bold=True)
        self.label_colour = label_colour
        self.press_drop = True

    def update(self, mouse_position):
        if not self.enabled:
            self.hovered = False
            return
        self.hovered = self.rect.collidepoint(mouse_position)

    def handle_event(self, event):
        if self.enabled and self.purpose is not None:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hovered:
                    self.pressed = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and self.pressed and self.hovered:
                    self.purpose()
                    self.pressed = False
            elif event.type == pg.MOUSEMOTION:
                if self.pressed and not self.hovered:
                    self.purpose()
                    self.pressed = False

    def draw(self, renderer):
        renderer.draw_basics(self)
        renderer.draw_text(self)


