import numpy as np
from pathlib import Path

class UIRenderer():
    def __init__(self, context, screen_size):
        self.program = None
        self.context = context
        self.screen_size = screen_size

        self.shade()
        self.make_geometry()

    def shade(self):
        shader_directory = (Path(__file__).parent/ "shaders")

        with open(shader_directory / "ui_vertex.glsl") as file:
            vertex_shader = file.read()

        with open(shader_directory / "ui_fragment.glsl") as file:
            fragment_shader = file.read()

        self.program = self.context.program(
            vertex_shader = vertex_shader,
            fragment_shader = fragment_shader
        )

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

        self.vbo = self.context.buffer(vertices.tobytes())
        self.vao = self.context.simple_vertex_array(self.program, self.vbo, "base_position")

    def draw_element(self, element):
        self.program["position"].value = element.position
        self.program["size"].value = element.size
        self.program["screen_size"].value = self.screen_size

        self.program["colour"].value = element.colour
        self.program["radius"].value = element.corner_radius
        self.program["border_colour"].value = element.border_colour
        self.program["border_size"].value = element.border_size

        self.vao.render()