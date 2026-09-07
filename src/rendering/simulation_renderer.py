from pathlib import Path
import numpy as np
from pyglm import glm

class Simulation_Renderer:
    def __init__(self, context, screen_size):
        self.context = context
        self.screen_size = screen_size
        self.radius_scale = 150_000.0
        self.distance_scale = 10_000_000.0

        self.sim_program = None

        self.shade()
        self.make_geometry()

    def triangles_and_normals(self, segments, rings):
        vertices = []
        normals = []
        # Creates arrays of all vertices and normals in the sphere
        for i in range(rings+1):
            phi = (i / rings) * np.pi
            for j in range(segments + 1):
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
                indices.extend([p1, p2, p1+1, p1+1, p2, p2+1]) # creates 2 complementing triangles so that they form a square

        vertex_data = np.hstack( # matches each triangle with its normal
            [np.array(vertices, dtype="f4"). reshape(-1,3),
            np.array(normals, dtype="f4").reshape(-1, 3)]
        ).flatten()
        indices_data = np.array(indices, dtype="i4")

        return vertex_data, indices_data

    def shade(self):
        shader_directory = (Path(__file__).parent/ "shaders")

        with open(shader_directory / "sim_vertex.glsl") as file:
            vertex_shader = file.read()

        with open(shader_directory / "sim_fragment.glsl") as file:
            fragment_shader = file.read()

        self.sim_program = self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    def make_geometry(self):
        vertex_data, indices_data = self.triangles_and_normals(32, 26)
        self.vbo = self.context.buffer(vertex_data)
        self.ibo = self.context.buffer(indices_data)
        self.vao = self.context.simple_vertex_array(self.sim_program, self.vbo, "in_position", "in_normal", index_buffer=self.ibo)

    def draw(self, body):
        gl_radius = body.radius / self.radius_scale
        #gl_radius = max(gl_radius, 0.4)

        # Parameters: fov, aspect ratio, near clipping (nearest point visible), far clipping (furthest point visible)
        proj_matrix = glm.perspective(glm.radians(45.0), self.screen_size[0] / self.screen_size[1], 0.1, 10000000.0)
        view_matrix = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -30.0)) # Last number is camera offset, will be variable

        pos_x = body.position[0] / self.distance_scale
        pos_y = body.position[1] / self.distance_scale
        pos_z = body.position[2] / self.distance_scale

        model_matrix = glm.mat4(1.0) # blank
        model_matrix = glm.translate(model_matrix, glm.vec3(pos_x, pos_y, pos_z))
        model_matrix = glm.scale(model_matrix, glm.vec3(gl_radius, gl_radius, gl_radius))

        self.sim_program["m_proj"].write(proj_matrix)
        self.sim_program["m_view"].write(view_matrix)
        self.sim_program["m_model"].write(model_matrix)

        self.sim_program['light_dir'].value = (0.0, 0.0, 1.0)
        self.sim_program['body_colour'].value = body.colour

        self.vao.render()