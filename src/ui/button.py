import pygame as pg
import moderngl
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

    def draw(self, renderer):

        offset = 3.0 if self.pressed else 0.0

        renderer
        renderer.ui_program["position"].value = (self.position[0], self.position[1] + offset)
        renderer.ui_program["size"].value = self.size
        renderer.ui_program["screen_size"].value = renderer.screen_size

        renderer.ui_program["colour"].value = self.colour
        renderer.ui_program["border_colour"].value = self.border_colour
        renderer.ui_program["radius"].value = self.corner_radius
        renderer.ui_program["border_size"].value = self.border_size

        renderer.ui_program["enable_shadow"].value = self.enable_shadow
        if self.enable_shadow:
            if self.pressed:
                renderer.ui_program["shadow_offset"].value = (0.0, 2.0)
                renderer.ui_program["shadow_blur"].value = 4.0
            else:
                renderer.ui_program["shadow_offset"].value = (0.0, 4.0)
                renderer.ui_program["shadow_blur"].value = 8.0

        renderer.ui_vao.render()

        if self.label is not None:
            if self.text_texture is None:
                text = self.font.render(self.label, True, self.label_colour)
                self.text_size = text.get_size()
                pixel_data = pg.image.tobytes(text, "RGBA")
                self.text_texture = renderer.context.texture(self.text_size, 4, pixel_data)
                self.text_texture.filter = (moderngl.LINEAR, moderngl.LINEAR)

        text_x = self.position[0] + (self.size[0] - self.text_size[0]) * 0.5
        text_y = self.position[1] + (self.size[1] - self.text_size[1]) * 0.5

        renderer.text_program["position"].value = text_x, text_y + offset
        renderer.text_program["size"].value = self.text_size
        renderer.text_program["screen_size"].value = renderer.screen_size

        self.text_texture.use(0)
        renderer.text_program["text_texture"].value = 0

        renderer.text_vao.render()

