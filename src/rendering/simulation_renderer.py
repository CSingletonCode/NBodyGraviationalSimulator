from pathlib import Path
import moderngl
import numpy as np

from constants import DISTANCE_SCALE

class SimulationRenderer:
    def __init__(self, context, screen_size, camera):
        self.context = context
        self.screen_size = screen_size
        self.camera = camera
        self.proportional_radius = False

        self.sim_program = None
        self.trail_program = None
        self.trail_vbo = context.buffer(reserve=60000) # Space stored to hold 5000 points

        self.shade()
        self.make_geometry()

    def triangles_and_normals(self, segments, rings):
        """Produces the trangles and normals for a unit sphere. """
        vertices = []
        normals = []
        # Creates arrays of all vertices and normals in the sphere
        for i in range(rings + 1):
            phi = (i / rings) * np.pi # The angle at each ring from the top to bottom of the sphere
            for j in range(segments + 1):
                theta = (j / segments) * 2 * np.pi # The angle at each segment around the sphere
                # Calculates the 3D Cartesian coordinates from the spherical coordinates
                x = np.cos(theta) * np.sin(phi)
                y = np.cos(phi)
                z = np.sin(theta) * np.sin(phi)
                vertices.extend([x, y, z]) # Stores the positions
                normals.extend([x, y, z]) # For a unit sphere the normals are the same as the coordinates

        indices = []
        # Generates indices to identify how each vertex needs to be read.
        for i in range(rings):
            for j in range(segments):
                p1 = i * (segments + 1) + j # Top leftmost vertex in each triangle
                p2 = p1 + segments + 1 # the vertex directly below p1 on the next segment
                indices.extend([p1, p1+1, p2, p1+1, p2+1, p2]) # creates 2 complementing triangles so that they form a square

        # matches each triangle with its normal, arranges the vertices and normals into a list of 3d lists
        vertex_data = np.hstack(
            [np.array(vertices, dtype="f4"). reshape(-1,3),
            np.array(normals, dtype="f4").reshape(-1, 3)]
        ).flatten()
        indices_data = np.array(indices, dtype="i4")

        return vertex_data, indices_data

    def shade(self):
        """Retrieves the shaders for the trails and bodies, creates the necessary programs from them"""
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
        """Makes the arrays and buffers of the vertices normals and their indices for the sphere."""
        vertex_data, indices_data = self.triangles_and_normals(32, 26)
        # Sends the vertex data and the corresponding indices to the gpu
        self.vbo = self.context.buffer(vertex_data)
        self.ibo = self.context.buffer(indices_data)
        # Sends the vertices and normals to the shader, the ibo tells the shader how to read them.
        self.vao = self.context.simple_vertex_array(self.sim_program, self.vbo, "in_position", "in_normal", index_buffer=self.ibo)
        # Sends the list of trail points to the shader.
        self.trail_vao = self.context.simple_vertex_array(self.trail_program, self.trail_vbo, "in_position")

    def draw(self, body):
        """Retrieves the projection, view and model matrices to position the 3D object on a 2D screen."""
        # The projection matrix, converts the 3D space into screen space, handles the perspective of objects at different distances and the fov.
        projection_matrix = self.camera.get_projection_matrix()
        # The view matrix, handles the cameras position and orientation.
        view_matrix = self.camera.get_view_matrix()
        # The model matrix, handles the size, position, tilt and rotation of the body.
        model_matrix = body.get_model_matrix(self.proportional_radius)

        self.sim_program["projection_matrix"].write(projection_matrix)
        self.sim_program["view_matrix"].write(view_matrix)
        self.sim_program["model_matrix"].write(model_matrix)
        self.sim_program['body_colour'].value = body.colour

        self.vao.render()

    def draw_trail(self, body):
        """Renders the stored points a body has travelled through as a white trail."""
        if len(body.trail) < 2 or not body.trail_on:
            return

        # Needed to position the points correctly.
        projection_matrix = self.camera.get_projection_matrix()
        view_matrix = self.camera.get_view_matrix()

        # Shrinks down the real world points to match the simulations scale
        scaled_points = np.array(body.trail, dtype="f4") / DISTANCE_SCALE
        self.trail_vbo.write(scaled_points) # Adds the stored points to the buffer

        self.trail_vao.program["projection_matrix"].write(projection_matrix)
        self.trail_vao.program["view_matrix"].write(view_matrix)

        self.context.line_width = 2.0 # Width of the trail
        # Specifies that the points are to be read and rendered as a connected line.
        self.trail_vao.render(moderngl.LINE_STRIP, vertices=len(body.trail))

