import pygame as pg

class Element:
    def __init__(self, location, dimensions, colour, border_colour, corner_radius):
        self.location = location
        self.dimensions = dimensions
        self.colour = colour
        self.border_colour = border_colour
        self.corner_radius = corner_radius
        self.rect = pg.Rect(location[0] - dimensions[0] // 2, location[1] - dimensions[1] // 2, dimensions[0], dimensions[1])

        self.visible = True
        self.enabled = True

        self.hovered = False
        self.pressed = False

    def hovering(self, mouse_position):
        if not self.enabled:
            self.hovered = False
            return

        self.hovered = self.rect.collidepoint(mouse_position)