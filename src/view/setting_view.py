import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from constants import *

class SettingView:
    def __init__(self, screen):
        self.screen = screen
        self.load_background_images()
        self.reset_clicked()
        

    def calculate_ratios(self):
        current_width, current_height = self.screen.get_size()
        return current_width / SCREEN_WIDTH, current_height / SCREEN_HEIGHT
    
    def init_ui_elements(self, grid_size):
        width_ratio, height_ratio = self.calculate_ratios()
        self.button_back_menu = Button(self.screen,1200 *width_ratio , 700 *height_ratio, 200 *width_ratio,100 *height_ratio, fontSize=30, margin=20,
                             inactiveColour=(245, 245, 245), pressedColour=(255, 255, 255), 
                             onClick=self.set_back_menu_clicked,image=self.load_image("assets/retour_from_setting.png",265 *width_ratio, 150 *height_ratio ),
                             imageHAlign='center')
        self.sliders = {
            "smart_rabbit": self.create_slider(int(500 *width_ratio),int(275*height_ratio),int(450 *width_ratio), int(16*height_ratio), 1, 3, 1, 1),
            "smart_fox": self.create_slider(int(500 *width_ratio),int(345*height_ratio),int(450 *width_ratio),int( 16*height_ratio), 1, 3, 1, 1),
            "start_rabbit": self.create_slider(int(500 *width_ratio),int(485*height_ratio),int(450 *width_ratio), int(16*height_ratio),1, grid_size//2, 1, grid_size//10),
            "start_fox": self.create_slider(int(500 *width_ratio),int(560*height_ratio),int(450 *width_ratio), int(16*height_ratio), 0, grid_size//5, 1, grid_size // 20),
            "spawn_carrot": self.create_slider(int(500 *width_ratio),int(700*height_ratio),int(450 *width_ratio),int( 16*height_ratio), 2, 20, 2, 10)
        }

    def create_slider(self, x, y, taille_x, taille_y, min_val, max_val, step, initial):
        return Slider(self.screen, x, y, taille_x, taille_y, min=min_val, max=max_val, step=step, initial=initial,
                      colour=(245,245,220), handleColour=(222,184,135))
        
    def load_background_images(self):
        width_ratio, height_ratio = self.calculate_ratios()
        self.background_image = self.load_image('assets/background_settings.jpg', self.screen.get_width(), self.screen.get_height())  
        self.setting_background = self.load_image("assets/panneau_setting.png", 800 * width_ratio , 800 * height_ratio)

    def load_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))
    
    def draw_text_slider(self, width_ratio, height_ratio):
        slider_positions = {
            'smart_rabbit': (int(1000 * width_ratio), int(280 * height_ratio)),
            'smart_fox': (int(1000 * width_ratio), int(352 * height_ratio)),
            'start_rabbit': (int(1000 * width_ratio), int(492 * height_ratio)),
            'start_fox': (int(1000 * width_ratio), int(567 * height_ratio)),
            'spawn_carrot' : (int(1000 * width_ratio), int(707 * height_ratio))
        }
        
        for name, (x, y) in slider_positions.items():
            slider = self.sliders[name]
            slider.draw()
            self.draw_text(str(slider.getValue()), x, y, font_size=int(36 * height_ratio))
    
    def draw_text(self, text, x, y, font_size=36):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (139, 69, 19))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def render(self):
        width_ratio, height_ratio = self.calculate_ratios()
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.setting_background, (300 * width_ratio, 0 *height_ratio))
        self.draw_text_slider(width_ratio, height_ratio)
        pygame_widgets.update(pygame.event.get())
        
    def set_back_menu_clicked(self):
        self.back_menu_clicked = True
    
    def reset_clicked(self):
        self.back_menu_clicked = False
    
    def get_slider_value(self, slider_name):
        return self.sliders[slider_name].getValue()
    
    def handle_event(self, event):
        pygame_widgets.update([event])
    
    def show_widgets(self):
        self.button_back_menu.show()
        for widget in self.sliders.values():
            widget.show()

    def hide_widgets(self):
        self.button_back_menu.hide()
        for widget in self.sliders.values():
            widget.hide()

    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.load_background_images()
        self.init_ui_elements()