import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from constants import *

class WelcomeView:
    def __init__(self, screen):
        self.screen = screen
        self.create_ui_elements()
        self.load_background_images()
        self.reset_clicked()
    
    def calculate_ratios(self):
        current_width, current_height = self.screen.get_size()
        return current_width / SCREEN_WIDTH, current_height / SCREEN_HEIGHT

    def create_ui_elements(self):
        width_ratio, height_ratio = self.calculate_ratios()
        
        button_width, button_height = 228 * width_ratio, 70 * height_ratio
        button_x = 584 * width_ratio
        
        self.button_start = self.create_button(button_x, 350 * height_ratio, 'assets/start.png', self.set_start_clicked, button_width, button_height)
        self.button_settings = self.create_button(button_x, 440 * height_ratio, 'assets/parametre.png', self.set_setting_clicked, button_width, button_height)

        slider_width, slider_height = int(200 * width_ratio), int(15 * height_ratio)
        slider_x = button_x
        slider_grid_y, slider_speed_y = int(610 * height_ratio), int(700 * height_ratio)

        self.slider_grid = self.create_slider(slider_x, slider_grid_y, slider_width, slider_height, 40, 150, 30, 40)
        self.slider_speed = self.create_slider(slider_x, slider_speed_y, slider_width, slider_height, 1, 10, 1, 1)

        self.font = pygame.font.Font(None, int(36 * height_ratio))
        self.draw_values_x = button_x + slider_width + 13
        self.draw_values_y1 = slider_grid_y - slider_height / 2
        self.draw_values_y2 = slider_speed_y - slider_height / 2

    def load_background_images(self):
        self.background_image = self.load_image('assets/background_welcome.jpg', self.screen.get_width(), self.screen.get_height())

    def load_image(self, path, width, height):
        return pygame.transform.scale(pygame.image.load(path), (width, height))
    
    def create_button(self, x, y, image_path, onclick_function, taille_x, taille_y):
        return Button(self.screen, x, y, taille_x, taille_y,
                      inactiveColour=(245, 245, 245), pressedColour=(245, 245, 245),hoverColour=(245, 245, 245),
                      radius=20, onClick=onclick_function, image=self.load_image(image_path, taille_x*1.4, taille_y*3.2),
                      imageHAlign='center', imageVAlign='center')

    def create_slider(self, x, y, taille_x, taille_y, min_val, max_val, step, initial):
        return Slider(self.screen, x, y, taille_x, taille_y, min=min_val, max=max_val, step=step, initial=initial,
                      colour=(245,245,220), handleColour=(222,184,135))

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_widgets()
        pygame_widgets.update(pygame.event.get())

    def draw_widgets(self):
        for widget in [self.button_start, self.slider_grid, self.slider_speed, self.button_settings]:
            widget.draw()
        self.draw_text(str(self.slider_grid.getValue()), self.draw_values_x, self.draw_values_y1)
        self.draw_text(str(self.slider_speed.getValue()), self.draw_values_x, self.draw_values_y2)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))

    def handle_event(self, event):
        pygame_widgets.update([event])
    
    def set_start_clicked(self):
        self.start_clicked = True
    
    def set_setting_clicked(self):
        self.setting_clicked = True

    def reset_clicked(self):
        self.start_clicked = False
        self.setting_clicked = False

    def get_grid_size(self):
        if self.slider_grid.getValue() == 60:
            return 50
        elif self.slider_grid.getValue() == 90:
            return 80
        elif self.slider_grid.getValue() == 120:
            return 100
        elif self.slider_grid.getValue() == 150:
            return 160
        return self.slider_grid.getValue()

    def get_speed(self):
        return self.slider_speed.getValue()

    def show_widgets(self):
        for widget in [self.button_start, self.button_settings, self.slider_grid, self.slider_speed]:
            widget.show()

    def hide_widgets(self):
        for widget in [self.button_start, self.slider_grid, self.slider_speed, self.button_settings]:
            widget.hide()
    
    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.load_background_images()
        self.create_ui_elements() 