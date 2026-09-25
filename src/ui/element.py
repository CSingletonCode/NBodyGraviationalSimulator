from constants import *


class Element:
    def __init__(self, position, size, colour, border_colour, corner_radius, border_size, enable_shadow):
        # Positioned from top left corner
        self.position = (position[0] * WIDTH_SCALE, position[1] * HEIGHT_SCALE)
        self.size = (size[0] * WIDTH_SCALE, size[1] * HEIGHT_SCALE)
        self.colour = colour
        self.border_colour = border_colour
        self.corner_radius = corner_radius
        self.border_size = border_size
        self.rect = pg.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.enable_shadow = enable_shadow
        self.text_texture = None
        self.press_drop = False
        self.visible = True
        self.enabled = True
        self.hovered = False

    def update(self, mouse_position):
        pass

    def handle_event(self, event):
        pass

    def interactable(self):
        return self.visible and self.enabled

    def disable(self):
        self.visible = False
        self.enabled = False

    def enable(self):
        self.enabled = True
        self.visible = True

    def freeze(self):
        self.enabled = False

    def unfreeze(self):
        self.enabled = True