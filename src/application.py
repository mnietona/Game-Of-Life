import random
import time
import pygame
from src.constants import *
from controller.welcome_controller import WelcomeController
from controller.grid_controller import GridController

class Application:
    def __init__(self):
        random.seed(int(time.time()))
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        pygame.display.set_caption("Game Of Life")
        self.controllers = {
            "welcome": WelcomeController(self),
        }
        self.current_controller = None
        self.switch_controller("welcome")

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.current_controller.handle_event(event)

            self.current_controller.render()
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    def switch_controller(self, controller_name, grid_size=None, speed=None):
        if controller_name == "grid":
            self.controllers["grid"] = GridController(self, grid_size, speed)
        self.current_controller = self.controllers[controller_name]
        self.current_controller.activate()

if __name__ == "__main__":
    app = Application()
    app.run()