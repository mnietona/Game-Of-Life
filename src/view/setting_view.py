import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

class SettingView:
    def __init__(self, screen):
        self.screen = screen
        self.init_ui_elements()
        self.back_menu_clicked = False
    
    def init_ui_elements(self):
        self.button_back_menu = Button(self.screen, 950, 700, 200, 40, fontSize=30, margin=20,
                             inactiveColour=(245, 245, 245), pressedColour=(255, 255, 255), 
                             onClick=self.set_back_menu_clicked,image=self.load_image("assets/retour.png", 320, 230),
                             imageHAlign='center')
        
    
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
        self.screen.fill((255, 255, 255))
        pygame_widgets.update(pygame.event.get())
    
    def show_widgets(self):
        self.button_back_menu.show()

    def hide_widgets(self):
        self.button_back_menu.hide()