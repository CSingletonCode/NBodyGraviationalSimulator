import pygame
import moderngl
import sys
from ui import UI

class App:
    def __init__(self):
        pygame.init()

        #Window Size Attributes
        self.info = pygame.display.Info()
        self.width, self.height = self.info.current_w, self.info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.display.set_caption("Orbit Model")

        #ModernGL Features
        self.context = moderngl.create_context()
        self.context.viewport = (0, 0, self.width, self.height)

        #Timing Attributes
        self.running = True
        self.clock = pygame.time.Clock()

        #self.renderer
        #self.simulation
        self.ui = UI(self.context)

    def run(self):
        while self.running:
            self.handleEvents()
            self.context.clear(0.6, 0.6, 0.6)
            self.ui.render()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui.handle_event(event)

#Closes the window -- Remove Self If No Changes Are Made Later
    def close(self):
        pygame.quit()
        sys.exit()