import numpy as np
import moderngl
from pathlib import Path
from constants import *

class UIRenderer:
    def __init__(self, context, screen_size):
        self.ui_program = None
        self.text_program = None
        self.context = context
        self.screen_size = screen_size
        self.ui_scale = float(min(HEIGHT_SCALE, WIDTH_SCALE))

        pg.font.init()

        self.shade()
        self.make_geometry()

    def shade(self):
        """Retrieves the renderers from their files, sets the pairs as the ui and text programs."""
        shader_directory = (Path(__file__).parent/ "shaders")

        with open(shader_directory / "ui_vertex.glsl") as file:
            vertex_shader = file.read()
        with open(shader_directory / "ui_fragment.glsl") as file:
            fragment_shader = file.read()
        with open(shader_directory / "text_vertex.glsl") as file:
            text_vertex = file.read()
        with open(shader_directory / "text_fragment.glsl") as file:
            text_fragment = file.read()

        self.ui_program = self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.text_program = self.context.program(vertex_shader=text_vertex, fragment_shader=text_fragment)

    def make_geometry(self):
        """Makes the numpy arrays for the rectangle shapes,
           Sends their data to the shaders. """
        # Simple rectangle of size 1 made of 2 triangles.
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

        # Sends the numpy array of vertices to the gpu.
        self.ui_vbo = self.context.buffer(vertices.tobytes())
        # Maps the vertex data to the shaders base_position in variable.
        self.ui_vao = self.context.simple_vertex_array(self.ui_program, self.ui_vbo, "base_position")

        # Makes a rectangle like above but also attaches texture coordinates in the corners.
        text_vertices = np.array(
            [
                # X,    Y,      U,   V
                -0.5, -0.5,     0.0, 0.0,
                0.5, -0.5,      1.0, 0.0,
                0.5, 0.5,       1.0, 1.0,

                -0.5, -0.5,     0.0, 0.0,
                0.5, 0.5,       1.0, 1.0,
                -0.5, 0.5,      0.0, 1.0
            ],
            dtype="f4"
        )

        # Sends the vertices and texture coordinates to the gpu
        self.text_vbo = self.context.buffer(text_vertices.tobytes())
        # Maps the vertex data and texture coordinates to the in variables in the shaders.
        self.text_vao = self.context.simple_vertex_array(self.text_program, self.text_vbo, "base_position", "in_uv")

    def draw_basics(self, element):
        """Draws the basic parts of an element, the shape, position, colour and shadow. """
        element.offset = 3.0 if element.pressed and element.press_drop else 0.0 # sets the position offset if the element has been pressed.

        self.ui_program["position"].value = (element.position[0], element.position[1] + element.offset)
        self.ui_program["size"].value = element.size
        self.ui_program["screen_size"].value = self.screen_size

        self.ui_program["colour"].value = element.colour
        self.ui_program["border_colour"].value = element.border_colour
        self.ui_program["radius"].value = element.corner_radius * self.ui_scale
        self.ui_program["border_size"].value = element.border_size * self.ui_scale

        self.ui_program["ui_scale"].value = self.ui_scale

        self.ui_program["enable_shadow"].value = element.enable_shadow

        # Changes the size and strength of the shadow if the element is pressed down.
        if element.enable_shadow:
            if element.pressed and element.press_drop:
                self.ui_program["shadow_offset"].value = (0.0, 2.0 * self.ui_scale)
                self.ui_program["shadow_blur"].value = 4.0 * self.ui_scale
            else:
                self.ui_program["shadow_offset"].value = (0.0, 4.0 * self.ui_scale)
                self.ui_program["shadow_blur"].value = 8.0 * self.ui_scale

        self.ui_vao.render()

    def draw_text(self, element):
        """Creates the texture for the label and positions it over the element. """
        if element.label is not None:
            if element.text_texture is None: # Remakes the texture whenever it is wiped.
                text = element.font.render(element.label, True, element.label_colour) # Renders the label as a pygame surface
                extended = pg.Surface((text.get_width(), text.get_height()) , pg.SRCALPHA) # creates a transparent pygame surface the same size as the label.
                extended.blit(text, (0, 0)) # Places the text on the surface
                element.text_size = extended.get_size()
                pixel_data = pg.image.tobytes(extended, "RGBA") # Gets the pixel data from the surface
                element.text_texture = self.context.texture(element.text_size, 4, pixel_data) # Sets the text as a texture
                # Stops the texture from repeating above or to the side
                element.text_texture.repeat_x = False
                element.text_texture.repeat_y = False
                # Smooths the texture linearly if its smaller or larger.
                element.text_texture.filter = (moderngl.LINEAR, moderngl.LINEAR)

            # Centres the label in the box
            text_x = element.position[0] + (element.size[0] - element.text_size[0]) * 0.5
            text_y = element.position[1] + (element.size[1] - element.text_size[1]) * 0.5

            self.text_program["position"].value = text_x, text_y + element.offset
            self.text_program["size"].value = element.text_size
            self.text_program["screen_size"].value = self.screen_size

            # Binds the texture to unit 0
            element.text_texture.use(0)
            # Tells OpenGL to read from unit 0
            self.text_program["text_texture"].value = 0

            self.text_vao.render()
