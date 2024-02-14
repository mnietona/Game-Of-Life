import pygame
from model.grid import Grid
from view.grid_view import GridView
from view.welcome_view import WelcomeView
from controller.grid_controller import GridController
from controller.welcome_controller import WelcomeController

class MainController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 816))
        pygame.display.set_caption("Game Of Life")
        self.init_views_and_controllers()
        self.click_sound = pygame.mixer.Sound("images/a.mp3")

    def init_views_and_controllers(self):
        self.views = {
            "main_menu": WelcomeView(self.screen, self.switch_to_grid_view),
            "grid": None 
        }
        self.controllers = {
            "main_menu": WelcomeController(self.views["main_menu"]),
            "grid": None
        }
        self.current_view = self.views["main_menu"]
        self.current_controller = self.controllers["main_menu"]

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

            # Mettre à jour la grille si le contrôleur actuel est GridController
            if isinstance(self.current_controller, GridController):
                self.current_controller.update()


            self.current_view.render()
            pygame.display.flip()

            # Limiter la vitesse de la boucle
            clock.tick(30)  # 30 mises à jour par seconde par exemple

        pygame.quit()

    def switch_to_grid_view(self):
        self.click_sound.play()
        grid_size = self.views["main_menu"].get_grid_size()
        speed = self.views["main_menu"].get_speed()
        rabbit_count = self.views["main_menu"].get_rabbit()
        fox_count = self.views["main_menu"].get_fox()
        self.grid = Grid(grid_size, speed,rabbit_count,fox_count)
        self.views["grid"] = GridView(self.screen, self.grid, self.switch_to_welcome_view)
        self.controllers["grid"] = GridController(self.grid, self.views["grid"])
        self.views["grid"].set_controller(self.controllers["grid"])
        
        self.switch_view("grid")
    
    def switch_to_welcome_view(self):
        self.click_sound.play()
        self.views["main_menu"] = WelcomeView(self.screen, self.switch_to_grid_view)
        self.controllers["main_menu"] = WelcomeController(self.views["main_menu"])
        self.switch_view("main_menu")
        

    def switch_view(self, view_name):
        if view_name == "main_menu":
            self.views["main_menu"].set_widget_active(True)
            self.views["grid"].set_widget_active(False)
        else:
            self.views["main_menu"].set_widget_active(False)
            self.views["grid"].set_widget_active(True)
        self.current_view = self.views[view_name]
        self.current_controller = self.controllers[view_name]
    
        
