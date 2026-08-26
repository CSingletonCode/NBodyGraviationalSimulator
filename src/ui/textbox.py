from ui.element import Element
import pygame as pg


class TextBox(Element):
    def __init__(self, position, size, colour, border_colour, label_colour, corner_radius, border_size,  writable, enable_shadow=False, label=""):
        super().__init__(position, size, colour, border_colour, corner_radius, border_size, enable_shadow)
        self.label = label
        self.label_colour = tuple(255*c for c in label_colour)
        self.writable = writable
        self.font_name = "Arial"
        self.label_size = 20
        self.bold = True
        self.font = pg.font.SysFont(self.font_name, self.label_size, self.bold)
        self.pressed = False
        self.focused = False
        self.limit = self.size[0] - self.border_size*2 - 10

    def update(self, mouse_position):
        if not self.enabled:
            self.hovered = False
            return
        self.hovered = self.rect.collidepoint(mouse_position)

    def handle_event(self, event):
        if self.enabled:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hovered:
                    self.pressed = True
                    self.focused = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and self.pressed and self.hovered:
                    self.pressed = False
            elif event.type == pg.MOUSEMOTION:
                if self.pressed and not self.hovered:
                    self.pressed = False

    def write(self, event):
        if not self.writable or not self.focused:
            return
        if event.key == pg.K_BACKSPACE:
            self.label = self.label[:-1]
        elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
            self.focused = False
        elif event.unicode and event.unicode.isprintable():
            proposed_label = self.label + event.unicode
            if self.limit >= self.font.size(proposed_label)[0]:
                self.label = proposed_label
        self.text_texture = None

    def draw(self, renderer):
        renderer.draw_basics(self)
        renderer.draw_text(self)

