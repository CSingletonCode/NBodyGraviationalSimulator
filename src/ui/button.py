import pygame as pg
from ui.element import Element
from constants import WIDTH_SCALE, HEIGHT_SCALE


class Button(Element):
    def __init__(self, position, size, purpose, colour, border_colour, label, label_colour, corner_radius, border_size, enable_shadow):
        super().__init__(position, size, colour, border_colour, corner_radius, border_size, enable_shadow)
        self.purpose = purpose
        self.label = label
        self.text_texture = None
        self.pressed = False
        self.font = pg.font.SysFont("Arial", int(20 * float(min(WIDTH_SCALE, HEIGHT_SCALE))), bold=True) # Scales text size with the resolution
        self.label_colour = tuple(255*colour for colour in label_colour) # Converts normalised RGB to 8-bit RGB scale
        self.press_drop = True

    def update(self, mouse_position):
        """Determines if the mouse is over the button."""
        if not self.enabled:
            self.hovered = False
            return
        self.hovered = self.rect.collidepoint(mouse_position)

    def handle_event(self, event):
        """Handles the pressing and releasing of the button."""
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


