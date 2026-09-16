import pygame
import moderngl
import sys
from ui.ui_manager import Manager
from rendering.ui_renderer import UIRenderer
from simulation.simulation_manager import Sim_Manager
from rendering.simulation_renderer import Simulation_Renderer
from ui.constants import *
from assets. colours import DARKBLUE
from rendering.camera import Camera

class App:
    def __init__(self):
        #Screen Size
        self.width, self.height = ACTIVE_RESOLUTION.current_w, ACTIVE_RESOLUTION.current_h

        pg.key.set_repeat(400, 50)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.display.set_caption("Orbit Model")

        #ModernGL Features
        self.context = moderngl.create_context()
        self.context.viewport = (0, 0, self.width, self.height)
        self.context.enable(moderngl.BLEND)
        self.context.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)
        self.context.enable(moderngl.DEPTH_TEST)
        self.context.enable(moderngl.CULL_FACE)

        #Timing Attributes
        self.running = True
        self.clock = pygame.time.Clock()

        self.simulation = Sim_Manager()
        self.camera = Camera(self.width, self.height)
        self.sim_renderer = Simulation_Renderer(self.context, (self.width, self.height), self.camera)
        self.manager = Manager((self.width, self.height), self.simulation)
        self.ui_renderer = UIRenderer(self.context, (self.width, self.height))


    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.event_loop(dt)
            if not self.manager.new_body_panel_state():
                self.camera.slide(dt)
            self.camera.update(dt)
            mouse_position = pygame.mouse.get_pos()
            self.manager.update_elements(mouse_position)
            self.context.clear(*DARKBLUE, depth=1.0)

            self.context.enable(moderngl.DEPTH_TEST)
            self.context.enable(moderngl.CULL_FACE)
            self.simulation.render(self.sim_renderer)

            self.context.disable(moderngl.DEPTH_TEST)
            self.context.disable(moderngl.CULL_FACE)
            self.manager.render(self.ui_renderer)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def event_loop(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.manager.handle_event(event)
            if not self.manager.new_body_panel_state():
                self.camera.handle_event(event, dt)


