import pygame


class PaintObject:

    def __init__(self, caption):
        self.is_running = False
        self.pygame_init(caption)

    def pygame_init(self, caption):
        pygame.init()
        window_width = 500
        window_height = 400
        pixel_size = 1
        window_size = (window_width * pixel_size, window_height * pixel_size)
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(caption)
        self.window.fill((255, 255, 255))
        pygame.display.update()

    def painting_update(self):
        pass

    def run(self):
        self.is_running = True
        while self.is_running:
            self.painting_update()
            pygame.display.update()
        pygame.quit()
