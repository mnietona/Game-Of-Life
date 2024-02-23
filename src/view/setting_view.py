import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from constants import *

class SettingView:
    def __init__(self, screen):
        self.screen = screen
        self.init_ui_elements()
        
        self.load_background_images()
        self.back_menu_clicked = False

    def calculate_ratios(self):
        current_width, current_height = self.screen.get_size()
        return current_width / SCREEN_WIDTH, current_height / SCREEN_HEIGHT

    def init_ui_elements(self):
        width_ratio, height_ratio = self.calculate_ratios()
        self.button_back_menu = Button(self.screen,1200 *width_ratio , 700 *height_ratio, 200 *width_ratio,100 *height_ratio, fontSize=30, margin=20,
                             inactiveColour=(245, 245, 245), pressedColour=(255, 255, 255), 
                             onClick=self.set_back_menu_clicked,image=self.load_image("assets/retour_from_setting.png",265 *width_ratio, 150 *height_ratio ),
                             imageHAlign='center')
        
        self.slider_smart_rabbit = self.create_slider(int(500 *width_ratio),int(275*height_ratio),int(450 *width_ratio), int(16*height_ratio),0, 2, 1, 1)
        self.slider_smart_fox = self.create_slider(int(500 *width_ratio),int(345*height_ratio),int(450 *width_ratio),int( 16*height_ratio), 0, 2, 1, 1) 
        self.slider_start_rabbit = self.create_slider(int(500 *width_ratio),int(485*height_ratio),int(450 *width_ratio), int(16*height_ratio),1, 20, 1, 10)  #à définir
        self.slider_start_fox = self.create_slider(int(500 *width_ratio),int(560*height_ratio),int(450 *width_ratio), int(16*height_ratio), 1, 20, 1, 10) #à définir
        self.slider_spawn_carrot = self.create_slider(int(500 *width_ratio),int(700*height_ratio),int(450 *width_ratio),int( 16*height_ratio),2, 10, 1, 6)

        self.slider = [ self.slider_spawn_carrot, self.slider_smart_fox, self.slider_smart_rabbit,self.slider_start_fox, self.slider_start_rabbit]


    def draw_text_slider(self):
        width_ratio, height_ratio = self.calculate_ratios()
        self.font = pygame.font.Font(None, int(36 * height_ratio))
        self.text_smart_rabbit = self.draw_text(str(self.slider_smart_rabbit .getValue()),int(1000*width_ratio),int(275*height_ratio))
        self.text_smart_fox = self.draw_text(str(self.slider_smart_fox .getValue()),int(1000*width_ratio),int(345*height_ratio))
        self.text_start_rabbit = self.draw_text(str(self.slider_start_rabbit .getValue()),int(1000*width_ratio),int(485*height_ratio))
        self.text_start_fox = self.draw_text(str(self.slider_start_fox .getValue()),int(1000*width_ratio),int(560*height_ratio))
        self.text_spawn_carrot  = self.draw_text(str(self.slider_spawn_carrot .getValue()),int(1000*width_ratio),int(700*height_ratio))
        

    def create_slider(self, x, y, taille_x, taille_y, min_val, max_val, step, initial):
        return Slider(self.screen, x, y, taille_x, taille_y, min=min_val, max=max_val, step=step, initial=initial,
                      colour=(245,245,220), handleColour=(222,184,135))
    
    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))


    def load_background_images(self):
        width_ratio, height_ratio = self.calculate_ratios()
        self.background_image = self.load_image('assets/background_settings.jpg', self.screen.get_width() *width_ratio, self.screen.get_height()*height_ratio)  
        self.setting_background = self.load_image("assets/panneau_setting.png", 800 *width_ratio , 800*height_ratio)

    
    def load_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))
    
    def set_back_menu_clicked(self):
        self.back_menu_clicked = True
    
    def reset_clicked(self):
        self.back_menu_clicked = False
    
    def handle_event(self, event):
        pygame_widgets.update([event])
        
    def render(self):
        width_ratio, height_ratio = self.calculate_ratios()
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.setting_background, (300 * width_ratio, 0 *height_ratio))
        self.draw_text_slider()
        pygame_widgets.update(pygame.event.get())
    
    def show_widgets(self):
        self.button_back_menu.show()
        for widget in self.slider:
            widget.show()

    def hide_widgets(self):
        self.button_back_menu.hide()
        for widget in self.slider:
            widget.hide()

    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.load_background_images()
        self.init_ui_elements()
    