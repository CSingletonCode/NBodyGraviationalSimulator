import numpy as np
import pygame as pg
import moderngl
from pathlib import Path

class UIRenderer:
    def __init__(self, context, screen_size):
        self.ui_program = None
        self.text_program = None
        self.context = context
        self.screen_size = screen_size
        self.font = pg.font.SysFont("Arial", 20, bold=True)

        pg.font.init()

        self.shade()
        self.make_geometry()

    def shade(self):
        shader_directory = (Path(__file__).parent/ "shaders")

        with open(shader_directory / "ui_vertex.glsl") as file:
            vertex_shader = file.read()

        with open(shader_directory / "ui_fragment.glsl") as file:
            fragment_shader = file.read()

        with open(shader_directory / "text_vertex.glsl") as file:
            text_vertex = file.read()

        with open(shader_directory / "text_fragment.glsl") as file:
            text_fragment = file.read()

        self.ui_program = self.context.program(vertex_shader = vertex_shader, fragment_shader = fragment_shader)
        self.text_program = self.context.program(vertex_shader=text_vertex, fragment_shader=text_fragment)

    def make_geometry(self):
        vertices = np.array(
            [
                -0.5, -0.5,
                0.5, -0.5,
                0.5, 0.5,

                -0.5, -0.5,
                0.5, 0.5,
                -0.5, 0.5
            ],
            dtype="f4"
        )

        self.ui_vbo = self.context.buffer(vertices.tobytes())
        self.ui_vao = self.context.simple_vertex_array(self.ui_program, self.ui_vbo, "base_position")

        # Text Geometry (X, Y, U, V) - Adds texture mapping coordinates
        text_vertices = np.array(
            [
                # X,    Y,      U,   V (Texture Coordinates)
                -0.5, -0.5,     0.0, 0.0,
                0.5, -0.5,      1.0, 0.0,
                0.5, 0.5,       1.0, 1.0,

                -0.5, -0.5,     0.0, 0.0,
                0.5, 0.5,       1.0, 1.0,
                -0.5, 0.5,      0.0, 1.0
            ],
            dtype="f4"
        )
        self.text_vbo = self.context.buffer(text_vertices.tobytes())
        self.text_vao = self.context.simple_vertex_array(self.text_program, self.text_vbo, "base_position", "in_uv")

    def draw_basics(self, element):
        element.offset = 3.0 if element.pressed and element.press_drop else 0.0

        self.ui_program["position"].value = (element.position[0], element.position[1] + element.offset)
        self.ui_program["size"].value = element.size
        self.ui_program["screen_size"].value = self.screen_size

        self.ui_program["colour"].value = element.colour
        self.ui_program["border_colour"].value = element.border_colour
        self.ui_program["radius"].value = element.corner_radius
        self.ui_program["border_size"].value = element.border_size

        self.ui_program["enable_shadow"].value = element.enable_shadow
        if  element.enable_shadow:
            if element.pressed and element.press_drop:
                self.ui_program["shadow_offset"].value = (0.0, 2.0)
                self.ui_program["shadow_blur"].value = 4.0
            else:
                self.ui_program["shadow_offset"].value = (0.0, 4.0)
                self.ui_program["shadow_blur"].value = 8.0

        self.ui_vao.render()

    def draw_text(self, element):
        if element.label is not None:
            if element.text_texture is None:
                text = element.font.render(element.label, True, element.label_colour)
                extended = pg.Surface((text.get_width(), text.get_height()+4), pg.SRCALPHA)
                extended.blit(text, (0, 0))
                element.text_size = extended.get_size()
                pixel_data = pg.image.tobytes(extended, "RGBA")
                element.text_texture = self.context.texture(element.text_size, 4, pixel_data)
                element.text_texture.repeat_x = False
                element.text_texture.repeat_y = False
                element.text_texture.filter = (moderngl.LINEAR, moderngl.LINEAR)

            text_x = element.position[0] + (element.size[0] - element.text_size[0]) * 0.5
            text_y = element.position[1] + (element.size[1] - element.text_size[1]) * 0.5

            self.text_program["position"].value = text_x, text_y + element.offset
            self.text_program["size"].value = element.text_size
            self.text_program["screen_size"].value = self.screen_size

            element.text_texture.use(0)
            self.text_program["text_texture"].value = 0

            self.text_vao.render()
