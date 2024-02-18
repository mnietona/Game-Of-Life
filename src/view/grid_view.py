import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from constants import *

class GridView:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.size = grid.size
        self.cell_size =  SCREEN_HEIGHT // self.size
        self.font = pygame.font.Font(None, 36)
        self.background_image = self.load_image('assets/background_grid.jpg', screen.get_width(), screen.get_height())
        self.info_box_background = self.load_image("assets/info_box.png", 340, 235)
        self.turn_background = self.load_image("assets/tour.png", 230,120)
        self.setting_background = self.load_image("assets/settings.png", 390,280)
        self.legend_background = self.load_image("assets/legende.png", 390,280)
        self.init_ui_elements()
        self.hide_widgets()
        self.back_clicked = False
        self.pause_play_clicked = False
        self.next_step_clicked = False
        self.selected_cell = None  
        self.selected_cell_info = ""
        self.turn = 0
        self.count_rabbit = 0
        self.count_fox = 0
        self.count_carrot = 0

    def init_ui_elements(self):
        
        self.button_back = Button(self.screen, 1115, 735, 65, 65, fontSize=30, margin=20,
                                  image=self.load_image("assets/return.png", 110, 90),
                                  radius = 90,onClick=self.set_back_clicked)

        self.button_pause = Button(self.screen, 1035, 30, 58, 58, fontSize=30, margin=20,
                                        image=self.load_image("assets/pause.png", 100, 80),
                                        onClick=self.set_pause_play_clicked, radius = 90)

        self.button_play = Button(self.screen, 1035, 30, 58, 58, fontSize=30, margin=20,
                                  image=self.load_image( "assets/play.png", 100, 80),
                                  onClick=self.set_pause_play_clicked, radius = 90)
        
        self.button_next_step = Button(self.screen, 1115, 30, 58, 58, fontSize=30, margin=20,
                                       image=self.load_image("assets/next.png", 100, 80),
                                       onClick=self.set_next_step_clicked, radius = 90)
        
        self.slider_speed = Slider(self.screen, 940, 287, 160, 15, min=1, max=10, step=1, initial=self.grid.speed,
                                   colour=(152, 251, 152), handleColour=(255, 192, 203))
        
        self.slider_smart_rabbit = Slider(self.screen, 940, 385, 160, 15, min=1, max=3, step=1, initial=self.grid.smart_level_rabbit,
                                   colour=(152, 251, 152), handleColour=(255, 192, 203))
        
        self.slider_smart_fox = Slider(self.screen, 940, 423, 160, 15, min=1, max=3, step=1, initial=self.grid.smart_level_fox,
                                   colour=(152, 251, 152), handleColour=(255, 192, 203))
        
    def set_turn(self, turn):
        self.turn = turn
    
    def set_count(self, count_rabbit, count_fox, count_carrot):
        self.count_rabbit = count_rabbit
        self.count_fox = count_fox
        self.count_carrot = count_carrot
 
    def set_back_clicked(self):
        self.back_clicked = True

    def set_pause_play_clicked(self):
        self.pause_play_clicked = not self.pause_play_clicked
        self.update_buttons_based_on_pause_state(self.pause_play_clicked)
    
    def update_buttons_based_on_pause_state(self, is_paused):
        if is_paused:
            self.button_play.show()
            self.button_pause.hide()
        else:
            self.button_pause.show()
            self.button_play.hide()
            
    def set_next_step_clicked(self):
        self.next_step_clicked = True

    def load_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))
    
    def draw_widgets(self):
        self.draw_info_box()
        self.draw_turn()
        self.draw_legend()
        self.draw_settings()
    
    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_cells()
        self.draw_widgets()
        pygame_widgets.update(pygame.event.get())

    def draw_settings(self):
        self.screen.blit(self.setting_background, (800, 210))
        
        self.slider_speed.draw()
        self.draw_text(str(self.slider_speed.getValue()), 1128, 293)
        
        self.slider_smart_rabbit.draw()
        self.draw_text(str(self.slider_smart_rabbit.getValue()), 1128, 391)
        
        self.slider_smart_fox.draw()
        self.draw_text(str(self.slider_smart_fox.getValue()), 1128, 429)
        
        
    def draw_legend(self):
        self.screen.blit(self.legend_background, (800, 460))
        self.draw_text(f"{self.count_carrot}", 995, 520)
        self.draw_text(f"{self.count_rabbit}", 995, 600)
        self.draw_text(f"{self.count_fox}", 995, 680)
    
    def draw_turn(self):
        self.screen.blit(self.turn_background, (800, 0))
        self.draw_text(f"{self.turn}", 918, 77)

    def draw_info_box(self):
        self.screen.blit(self.info_box_background, (830, 40))
        
        if self.selected_cell:
            text_y = 140  # Démarre le texte un peu plus bas dans la boîte d'informations
            lines = self.selected_cell_info.split('- ')
            for line in lines:
                self.draw_text(line, 1005, text_y, font_size=24)
                text_y += 30

    def draw_cells(self):
        for i in range(self.size):
            for j in range(self.size):
                rect = pygame.Rect(10 + j * self.cell_size, 10 + i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.get_cell_color(i, j), rect)
                pygame.draw.rect(self.screen, (0, 90, 0), rect, 1) 

    def get_cell_color(self, i, j):
        cell_element = self.grid.cells[i][j].element
        return cell_element.color
    
    def get_speed(self):
        return self.slider_speed.getValue()
    
    def get_smart_rabbit(self):
        return self.slider_smart_rabbit.getValue()
    
    def get_smart_fox(self):
        return self.slider_smart_fox.getValue()

    def draw_text(self, text, x, y, font_size=36):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (139, 69, 19))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        pygame_widgets.update([event])
    
    def show_widgets(self):
        self.button_back.show()
        self.button_pause.show()
        self.button_next_step.show()
        self.slider_speed.show()
        
    def hide_widgets(self):
        self.button_back.hide()
        self.button_pause.hide()
        self.button_play.hide()
        self.button_next_step.hide()
        self.slider_speed.hide()

    def reset_button_clicks(self):
        self.back_clicked = False
        self.next_step_clicked = False
        self.pause_play_clicked = False

