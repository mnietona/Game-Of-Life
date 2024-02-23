import random, time, pygame, sys
from constants import *
from controller.welcome_controller import WelcomeController
from controller.grid_controller import GridController
from controller.setting_controller import SettingController

class Application:
    def __init__(self):
        random.seed(int(time.time()))
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Game Of Life")
        self.controllers = {
            "welcome": WelcomeController(self),
            "grid": None, 
            "setting": SettingController(self),
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
                elif event.type == pygame.VIDEORESIZE:
                    self.current_controller.resize_screen(event.w, event.h)
                else:
                    self.current_controller.handle_event(event) 

            self.current_controller.render()
            pygame.display.flip()
            clock.tick(FPS)

        self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit()


    def switch_controller(self, controller_name, grid_size=None, speed=None, smart_level_fox=None, smart_level_rabbit=None, default_rabbits=None, default_foxes=None, default_carrot_spawn=None):
        if controller_name == "grid":
            self.controllers["grid"] = GridController(self, grid_size, speed, smart_level_fox, smart_level_rabbit, default_rabbits, default_foxes, default_carrot_spawn)
        self.current_controller = self.controllers[controller_name]
        self.current_controller.activate()

if __name__ == "__main__":
    app = Application()
    app.run()