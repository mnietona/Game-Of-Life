import pygame
from view.grid_view import GridView

class GridController:
    def __init__(self, app):
        self.app = app
        self.view = GridView(app.screen, self.back_to_welcome)

    def activate(self):
        # Initialisation ou réinitialisation spécifique de la vue
        pass

    def back_to_welcome(self):
        self.app.switch_controller("welcome")

    def handle_event(self, event):
        self.view.handle_event(event)

    def render(self):
        self.view.render()
