import pygame
import moderngl
import sys

from simulation.physics import Physics_Engine
from ui.ui_manager import Manager
from rendering.ui_renderer import UIRenderer
from simulation.simulation_manager import SimManager
from rendering.simulation_renderer import SimulationRenderer
from constants import *
from colours import DARKBLUE
from rendering.camera import Camera

class App:
    def __init__(self):
        #Screen Size
        self.width, self.height = ACTIVE_RESOLUTION.current_w, ACTIVE_RESOLUTION.current_h

        # Input delay for holding down keys
        pg.key.set_repeat(400, 50)

        # Enables multisampling anti aliasing.
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1) # Available buffers
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4) # Samples per pixel

        # Creates an OpenGL window with double buffering
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)

        self.context = moderngl.create_context() # Creates moderngl context
        self.context.viewport = (0, 0, self.width, self.height) # Sizes to entire screen

        # Enables colours to be blended with alpha values
        self.context.enable(moderngl.BLEND)
        self.context.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)

        self.running = True
        self.clock = pygame.time.Clock()

        self.simulation = SimManager()
        self.camera = Camera(self.width, self.height)
        self.physics = Physics_Engine(self.simulation.bodies)
        self.sim_renderer = SimulationRenderer(self.context, (self.width, self.height), self.camera)
        self.manager = Manager((self.width, self.height), self.simulation, self.camera)
        self.ui_renderer = UIRenderer(self.context, (self.width, self.height))

    def run(self):
        """Contains the main loop of the simulation"""
        while self.running:
            speed_index = self.manager.get_speed_index() # Speed set by user
            time_scale = SPEEDS[speed_index] # seconds multiplier
            steps_num = SUBSTEPS[speed_index] # Amount of loops each tick is broken into to calculate positions accurately
            dt = time_scale * self.clock.tick(60) / 1000.0
            paused = self.manager.get_pause_state()

            if not paused:
                self.physics.update_bodies(dt, steps_num) # Gets new speeds and locations for all orbiting bodies

            self.event_loop(dt)

            if not self.manager.new_body_panel_state(): # Blocks the keyboard camera controls if the new body panel is open
                self.camera.slide(dt/time_scale)

            self.camera.update(dt) # Moves camera to correct position
            mouse_position = pygame.mouse.get_pos()
            self.manager.update_elements(mouse_position) # Checks for mouse collisions with UI
            self.context.clear(*DARKBLUE, depth=1.0)

            self.context.enable(moderngl.DEPTH_TEST)  # Allows OpenGL to determine what objects are in front of each other
            self.context.enable(moderngl.CULL_FACE)  # Removes surfaces pointing away from the screen
            self.simulation.render(self.sim_renderer, paused, dt) # Adds orbiting bodies to the screen

            # Removes depth test and face culling for UI components, ensures they renderer in the correct layers
            self.context.disable(moderngl.DEPTH_TEST)
            self.context.disable(moderngl.CULL_FACE)
            self.manager.render(self.ui_renderer)
            pygame.display.flip() # Switches the buffer to add the new screen.

        pygame.quit()
        sys.exit()

    def event_loop(self, dt):
        """Passes all mouse and keyboard events to the ui components and camera"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.manager.handle_event(event) # UI button presses
            if not self.manager.new_body_panel_state():
                self.camera.handle_event(event, dt) # Camera movement if the pop-up is closed