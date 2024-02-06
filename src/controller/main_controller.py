import pygame
from model.grid import Grid
from view.main_menu import MainMenu
from view.grid_view import GridView
from controller.menu_controller import MenuController
from controller.grid_controller import GridController
import pygame_widgets

class MainController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 816))
        pygame.display.set_caption("Ecosstemme Pixel")
        self.grid = Grid(50, 20)
        self.views = {
            "main_menu": MainMenu(self.screen, self.switch_to_grid_view),
            "grid": GridView(self.screen, self.grid)
        }
        self.controllers = {
            "main_menu": MenuController(self.views["main_menu"]),
            "grid": GridController(self.grid, self.views["grid"])
        }

        self.current_view = self.views["main_menu"]
        self.current_controller = self.controllers["main_menu"]

    def switch_view(self, view_name):
        if view_name == "main_menu":
            self.views["main_menu"].set_widget_active(True)
        else:
            self.views["main_menu"].set_widget_active(False)
            
        self.current_view = self.views[view_name]
        self.current_controller = self.controllers[view_name]

    def switch_to_grid_view(self):
        
        grid_size = self.views["main_menu"].get_grid_size()
        temperature = self.views["main_menu"].get_temperature()

        self.grid = Grid(grid_size, temperature)
        
        self.views["grid"] = GridView(self.screen, self.grid)

        self.switch_view("grid")

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            self.current_view.render()
            pygame_widgets.update(events)
            pygame.display.flip()

        pygame.quit()
