from pathlib import Path

import moderngl
import numpy as np
from pyglm import glm

from constants import DISTANCE_SCALE

class Simulation_Renderer:
    def __init__(self, context, screen_size, camera):
        self.context = context
        self.screen_size = screen_size
        self.camera = camera
        self.proportional_radius = False

        self.sim_program = None
        self.trail_program = None
        self.trail_vbo = context.buffer(reserve=60000)

        self.shade()
        self.make_geometry()

    def triangles_and_normals(self, segments, rings):
        vertices = []
        normals = []
        # Creates arrays of all vertices and normals in the sphere
        for i in range(rings+1):
            v = 1.0 - (i / rings)
            phi = (i / rings) * np.pi
            for j in range(segments + 1):
                u = j / segments
                theta = (j / segments) * 2 * np.pi
                x = np.cos(theta) * np.sin(phi)
                y = np.cos(phi)
                z = np.sin(theta) * np.sin(phi)
                vertices.extend([x, y, z])
                normals.extend([x, y, z])

        indices = []
        # Connects all the vertices
        for i in range(rings):
            for j in range(segments):
                p1 = i * (segments + 1) + j # first point
                p2 = p1 + segments + 1 # point directly below first on next segment
                indices.extend([p1, p1+1, p2, p1+1, p2+1, p2]) # creates 2 complementing triangles so that they form a square

        vertex_data = np.hstack( # matches each triangle with its normal
            [np.array(vertices, dtype="f4"). reshape(-1,3),
            np.array(normals, dtype="f4").reshape(-1, 3)
             ]
        ).flatten()
        indices_data = np.array(indices, dtype="i4")

        return vertex_data, indices_data

    def shade(self):
        shader_directory = (Path(__file__).parent/ "shaders")

        with open(shader_directory / "sim_vertex.glsl") as file:
            vertex_shader = file.read()

        with open(shader_directory / "sim_fragment.glsl") as file:
            fragment_shader = file.read()

        with open(shader_directory / "trail_vertex.glsl") as file:
            trail_vertex_shader = file.read()

        with open(shader_directory / "trail_fragment.glsl") as file:
            trail_fragment_shader = file.read()

        self.sim_program = self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.trail_program = self.context.program(vertex_shader=trail_vertex_shader, fragment_shader=trail_fragment_shader)

    def make_geometry(self):
        vertex_data, indices_data = self.triangles_and_normals(32, 26)
        self.vbo = self.context.buffer(vertex_data)
        self.ibo = self.context.buffer(indices_data)
        self.vao = self.context.simple_vertex_array(self.sim_program, self.vbo, "in_position", "in_normal", index_buffer=self.ibo)
        self.trail_vao = self.context.simple_vertex_array(self.trail_program, self.trail_vbo, "in_position")

    def draw(self, body):
        # Parameters: fov, aspect ratio, near clipping (nearest point visible), far clipping (furthest point visible)
        projection_matrix = self.camera.get_projection_matrix()
        view_matrix = self.camera.get_view_matrix()
        model_matrix = body.get_model_matrix(self.proportional_radius)

        self.sim_program["m_proj"].write(projection_matrix)
        self.sim_program["m_view"].write(view_matrix)
        self.sim_program["m_model"].write(model_matrix)
        self.sim_program['body_colour'].value = body.colour

        self.vao.render()

    def draw_trail(self, body):
        if len(body.trail) < 2 or not body.trail_on:
            return

        projection_matrix = self.camera.get_projection_matrix()
        view_matrix = self.camera.get_view_matrix()

        scaled_points = np.array(body.trail, dtype="f4") / DISTANCE_SCALE
        self.trail_vbo.write(scaled_points)

        self.trail_vao.program["projection_matrix"].write(projection_matrix)
        self.trail_vao.program["view_matrix"].write(view_matrix)

        self.context.line_width = 2.0
        self.trail_vao.render(moderngl.LINE_STRIP, vertices=len(body.trail))

