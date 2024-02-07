import pygame_widgets

class WelcomeController:
    def __init__(self, view):
        self.view = view

    def handle_event(self, events):
        # Mettre à jour les widgets avec les événements
        pygame_widgets.update(events)
