import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from src.constants import *

class GridView:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.size = grid.size
        self.cell_size =  SCREEN_HEIGHT // self.size
        self.font = pygame.font.Font(None, 36)
        self.background_image = self.load_image('assets/background_grid.jpg', screen.get_width(), screen.get_height())
        self.info_box_background = self.load_image("assets/info_box_bg.png", 650, 600)
        self.init_ui_elements()
        self.hide_widgets()
        self.back_clicked = False
        self.pause_play_clicked = False
        self.next_step_clicked = False
        self.selected_cell = None  
        self.selected_cell_info = ""

    def init_ui_elements(self):
        
        self.button_back = Button(self.screen, 900, 350, 200, 50, fontSize=30, margin=20,
                                  image=self.load_image("assets/retour.png", 320, 230),
                                  onClick=self.set_back_clicked)

        self.button_pause = Button(self.screen, 1025, 40, 80, 48, fontSize=30, margin=20,
                                        image=self.load_image("assets/Pause.png", 160, 160),
                                        onClick=self.set_pause_play_clicked)

        self.button_play = Button(self.screen, 1025, 40, 80, 48, fontSize=30, margin=20,
                                  image=self.load_image( "assets/Play.png", 160, 160),
                                  onClick=self.set_pause_play_clicked)
        
        self.button_next_step = Button(self.screen, 1115, 40, 80, 48, fontSize=30, margin=20,
                                       image=self.load_image("assets/Next.png", 160, 160),
                                       onClick=self.set_next_step_clicked)
        
        self.slider_speed = Slider(self.screen, 900, 450, 200, 15, min=1, max=10, step=1, initial=1,
                                   colour=(152, 251, 152), handleColour=(255, 192, 203))
 
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

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_cells()
        self.draw_info_box()
        self.slider_speed.draw()
        self.draw_text(str(self.slider_speed.getValue()), 1125, 450, self.font)
        pygame_widgets.update(pygame.event.get())

    def draw_info_box(self):
        self.screen.blit(self.info_box_background, (680, -100))
        
        if self.selected_cell:
            font = pygame.font.Font(None, 24)
            lines = self.selected_cell_info.split('- ')
            text_y = 180 # pareil si deplacer texte vers le bas ou haut
            
            for line in lines:
                text_surface = font.render(line, True, (0, 0, 0))
                text_width = text_surface.get_width()
                text_x = 1005 - (text_width / 2) # modif si deplacer texte vers gauche 
                self.screen.blit(text_surface, (text_x, text_y))
                
                text_y += font.get_height() + 5

    def draw_cells(self):
        for i in range(self.size):
            for j in range(self.size):
                rect = pygame.Rect(10 + j * self.cell_size, 10 + i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.get_cell_color(i, j), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  

    def get_cell_color(self, i, j):
        cell_element = self.grid.cells[i][j].element
        return cell_element.color
    
    def get_speed(self):
        return self.slider_speed.getValue()

    def draw_text(self, text, x, y, font):
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))
    
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

