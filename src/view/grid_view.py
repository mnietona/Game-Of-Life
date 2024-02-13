import pygame
import pygame_widgets
from pygame_widgets.button import Button

class GridView:
    def __init__(self, screen, on_back):
        self.screen = screen
        self.on_back = on_back
        self.button_back = Button(screen, 100, 250, 300, 100, text='Back', onClick=self.on_back)

    def handle_event(self, event):
        pygame_widgets.update(event)

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.button_back.draw()
