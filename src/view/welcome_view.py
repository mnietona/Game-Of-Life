import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

class WelcomeView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.init_ui_elements()
        self.load_background_images()
        self.reset_clicked()
        
    def init_ui_elements(self):
        self.init_buttons()
        self.init_sliders()

    def load_background_images(self):
        self.background_image = self.load_image('assets/background_welcome.jpg', self.screen.get_width(), self.screen.get_height())

    def init_buttons(self):
        self.button_start = self.create_button(470, 375, 'assets/start.png', self.set_start_clicked)
        self.button_settings = self.create_button(1000, 690, 'assets/setting.png', self.set_setting_clicked)

    def create_button(self, x, y, image_path, onclick_function):
        return Button(self.screen, x, y, 245, 65, fontSize=30, margin=20,
                      inactiveColour=(245, 245, 245), pressedColour=(255, 255, 255),
                      radius=20, onClick=onclick_function, image=self.load_image(image_path, 320, 250),
                      imageHAlign='center')

    def init_sliders(self):
        self.slider_grid = self.create_slider(470, 610, 30, 140, 10, 30)
        self.slider_speed = self.create_slider(470, 700, 1, 10, 1, 1)

    def create_slider(self, x, y, min_val, max_val, step, initial):
        return Slider(self.screen, x, y, 200, 15, min=min_val, max=max_val, step=step, initial=initial,
                      colour=(152, 251, 152), handleColour=(255, 192, 203))

    def load_image(self, path, width, height):
        return pygame.transform.scale(pygame.image.load(path), (width, height))

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_widgets()
        pygame_widgets.update(pygame.event.get())

    def draw_widgets(self):
        for widget in [self.button_start, self.slider_grid, self.slider_speed, self.button_settings]:
            widget.draw()
        self.draw_text(str(self.slider_grid.getValue()), 685, 605)
        self.draw_text(str(self.slider_speed.getValue()), 685, 695)

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
        return self.slider_grid.getValue()

    def get_speed(self):
        return self.slider_speed.getValue()

    def show_widgets(self):
        for widget in [self.button_start, self.slider_grid, self.slider_speed, self.button_settings]:
            widget.show()

    def hide_widgets(self):
        for widget in [self.button_start, self.slider_grid, self.slider_speed, self.button_settings]:
            widget.hide()
