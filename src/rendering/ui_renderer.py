import numpy as np
import pygame
import moderngl
from pathlib import Path

class UIRenderer():
    def __init__(self, context, screen_size):
        self.ui_program = None
        self.text_program = None
        self.context = context
        self.screen_size = screen_size
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

        pygame.font.init()


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

        # 2. Text Geometry (X, Y, U, V) - Adds texture mapping coordinates
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
