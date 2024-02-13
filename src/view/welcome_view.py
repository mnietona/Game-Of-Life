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
        self.font.set_bold(False)
        self.background_image = self.load_image('assets/background_welcom.jpg', screen.get_width(), screen.get_height())

    def init_ui_elements(self):
        self.button = Button(self.screen, 470, 375, 245, 65, text='', fontSize=30, margin=20, 
                             inactiveColour=(245, 245, 245), pressedColour=(255, 255, 255), 
                             radius=20, onClick=self.on_start, image=self.load_image("assets/start.png", 320, 250),
                             imageHAlign='center')
        self.slider_grid = Slider(self.screen, 470, 610, 200, 15, min=10, max=100, step=10, initial=50,
                                  colour=(152, 251, 152), handleColour=(255, 192, 203))
        self.slider_speed = Slider(self.screen, 470, 700, 200, 15, min=1, max=10, step=1, initial=5,
                                         colour=(152, 251, 152), handleColour=(255, 192, 203))

    def load_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.button.draw()
        self.slider_grid.draw()
        self.draw_text(str(self.slider_grid.getValue()), 685, 605, self.font)
        self.slider_speed.draw()
        self.draw_text(str(self.slider_speed.getValue()), 685, 695, self.font)
        pygame_widgets.update(pygame.event.get())

    def draw_text(self, text, x, y, font):
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))

    def get_grid_size(self):
        return self.slider_grid.getValue()

    def get_speed(self):
        return self.slider_speed.getValue()
    
    def set_widget_active(self, active):
        if active:
            self.button.show()
            self.slider_grid.show()
            self.slider_speed.show()
        else:
            self.button.hide()
            self.slider_grid.hide()
            self.slider_speed.hide()
