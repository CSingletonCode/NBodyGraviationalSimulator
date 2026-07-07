import pygame
import moderngl
import sys

class App:
    def run(self):
        pygame.init()

        info = pygame.display.Info()
        width, height = info.current_w, info.current_h

        screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Orbit Model")
        context = moderngl.create_context()
        context.viewport = (0, 0, width, height)

        clock = pygame.time.Clock()
#Test Comment
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            context.clear(1, 1, 1)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()