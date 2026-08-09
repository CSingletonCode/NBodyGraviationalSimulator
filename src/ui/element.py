import pygame as pg

class Element:
    def __init__(self, position, size, colour, border_colour, corner_radius, border_size):
        self.position = position # Positioned from top left corner
        self.size = size
        self.colour = colour
        self.border_colour = border_colour
        self.corner_radius = corner_radius
        self.border_size = border_size
        self.rect = pg.Rect(position[0], position[1], size[0], size[1])

        self.visible = True
        self.enabled = True

        self.hovered = False

    def update(self, mouse_position):
        pass

    def handle_event(self, event):
        pass

    @property
    def interactable(self):
        return self.visible and self.enabled