import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

class WelcomeView:
    def __init__(self, screen, on_start):
        self.screen = screen
        self.on_start = on_start
        self.init_ui_elements()
        self.font = pygame.font.Font(None, 36)
        self.font.set_bold(True)
        self.background_image = self.load_image('images/background2.jpg', screen.get_width(), screen.get_height())

    def init_ui_elements(self):
        # Initialiser les éléments de l'interface utilisateur ici
        self.button = Button(self.screen, 470, 375, 245, 65, text='', fontSize=30, margin=20, 
                             inactiveColour=(245, 245, 245), pressedColour=(255, 255, 255), 
                             radius=20, onClick=self.on_start, image=self.load_image("images/start.png", 320, 250),
                             imageHAlign='center')
        self.slider_grid = Slider(self.screen, 500, 600, 200, 15, min=10, max=100, step=10, initial=50,
                                  handleColour=(152, 251, 152), colour=(255, 192, 203))
        self.slider_temperature = Slider(self.screen, 500, 700, 200, 15, min=-10, max=50, step=5, initial=20,
                                         colour=(152, 251, 152), handleColour=(255, 192, 203))

    def load_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.button.draw()
        self.slider_grid.draw()
        self.draw_text(str(self.slider_grid.getValue()), 730, 605, self.font)
        self.slider_temperature.draw()
        self.draw_text(str(self.slider_temperature.getValue()), 730, 695, self.font)
        pygame_widgets.update(pygame.event.get())

    def draw_text(self, text, x, y, font):
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))

    def get_grid_size(self):
        return self.slider_grid.getValue()

    def get_temperature(self):
        return self.slider_temperature.getValue()
    
    def set_widget_active(self, active):
        if active:
            self.button.show()
            self.slider_grid.show()
            self.slider_temperature.show()
        else:
            self.button.hide()
            self.slider_grid.hide()
            self.slider_temperature.hide()
