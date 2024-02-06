import pygame
from model.grid import Grid
from view.main_menu import MainMenu
from view.grid_view import GridView
from controller.controller_main_menu import ControllerMainMenu
from controller.controller_grid import ControllerGrid

class MainController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400), pygame.RESIZABLE)
        pygame.display.set_caption("Game Of the Live")

        self.grid = Grid(100)  # Taille de la grille
        self.main_menu_view = MainMenu(self.screen)
        self.grid_view = GridView(self.screen, self.grid)

        self.main_menu_controller = ControllerMainMenu(self.main_menu_view)
        self.grid_controller = ControllerGrid(self.grid, self.grid_view)

        self.current_view = self.main_menu_view
        self.current_controller = self.main_menu_controller

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.current_view.resize(event.w, event.h)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_controller.handle_event(event):
                        self.current_view = self.grid_view
                        self.current_controller = self.grid_controller

            self.current_view.render()
            pygame.display.flip()

        pygame.quit()

