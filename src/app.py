import pygame
import moderngl
import sys
from ui import ui_manager
from rendering import ui_renderer
from ui.constants import *
from assets. colours import DARKBLUE

class App:
    def __init__(self):
        #Screen Size

        self.width, self.height = ACTIVE_RESOLUTION.current_w, ACTIVE_RESOLUTION.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.display.set_caption("Orbit Model")

        #ModernGL Features
        self.context = moderngl.create_context()
        self.context.viewport = (0, 0, self.width, self.height)
        self.context.enable(moderngl.BLEND)

        self.context.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA
        )

        #Timing Attributes
        self.running = True
        self.clock = pygame.time.Clock()

        self.manager = ui_manager.Manager((self.width, self.height))
        self.renderer = ui_renderer.UIRenderer(self.context, (self.width, self.height))
        #self.simulation

    def run(self):
        while self.running:
            self.handleEvents()
            mouse_position = pygame.mouse.get_pos()
            self.manager.update_elements(mouse_position)
            self.context.clear(*DARKBLUE)
            self.manager.render(self.renderer)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.manager.handle_event(event)
