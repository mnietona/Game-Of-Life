import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from constants import *

class GridView:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.cell_size = SCREEN_HEIGHT // self.grid.size
        self.font = pygame.font.Font(None, 36)
        self.load_background_images()
        self.init_values()
        self.reset_click_states()
        self.init_ui_elements()
        self.hide_widgets()

    def load_background_images(self):
        self.background_image = self.load_image('assets/background_grid.jpg', self.screen.get_width(), self.screen.get_height())
        self.info_box_background = self.load_image("assets/info_box.png", 340, 235)
        self.turn_background = self.load_image("assets/tour.png", 230, 120)
        self.setting_background = self.load_image("assets/settings.png", 390, 280)
        self.legend_background = self.load_image("assets/legende.png", 390, 280)

    def reset_click_states(self):
        self.back_clicked = False
        self.pause_play_clicked = False
        self.next_step_clicked = False
    
    def init_values(self):
        self.selected_cell = None  
        self.selected_cell_info = ""
        self.turn = 0
        self.count_rabbit = 0
        self.count_fox = 0
        self.count_carrot = 0

    def init_ui_elements(self):
        self.buttons = {
            'back': self.create_button(1115, 735, "assets/return.png", self.toggle_click_state, 'back_clicked'),
            'play': self.create_button(1035, 30, "assets/play.png", self.toggle_pause_play),
            'pause': self.create_button(1035, 30, "assets/pause.png", self.toggle_pause_play),
            'next_step': self.create_button(1115, 30, "assets/next.png", self.toggle_click_state, 'next_step_clicked')
        }
        
        self.sliders = {
            'speed': self.create_slider(940, 287, 1, 10, self.grid.speed),
            'smart_rabbit': self.create_slider(940, 385, 1, 3, self.grid.smart_level_rabbit),
            'smart_fox': self.create_slider(940, 423, 1, 3, self.grid.smart_level_fox)
        }

    def create_button(self, x, y, image_path, onclick_function, click_state=None):
        image = self.load_image(image_path, 100, 80)
        if click_state is not None:
            return Button(self.screen, x, y, 58, 58, fontSize=30, margin=20, image=image, onClick=lambda: onclick_function(click_state), radius=90)
        else:
            return Button(self.screen, x, y, 58, 58, fontSize=30, margin=20, image=image, onClick=onclick_function, radius=90)

    def create_slider(self, x, y, min_val, max_val, initial):
        return Slider(self.screen, x, y, 160, 15, min=min_val, max=max_val, step=1, initial=initial, colour=(152, 251, 152), handleColour=(255, 192, 203))

    def toggle_click_state(self, state):
        setattr(self, state, not getattr(self, state))

    def toggle_pause_play(self):
        self.pause_play_clicked = not self.pause_play_clicked
        self.update_buttons_based_on_pause_state(self.pause_play_clicked)
    
    def update_buttons_based_on_pause_state(self, is_paused):
        self.buttons['play'].show() if is_paused else self.buttons['pause'].show()
        self.buttons['pause'].hide() if is_paused else self.buttons['play'].hide()

    def load_image(self, path, width, height):
        return pygame.transform.scale(pygame.image.load(path), (width, height))

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_cells()
        self.draw_widgets()
        pygame_widgets.update(pygame.event.get())

    def draw_widgets(self):
        self.draw_info_box()
        self.draw_turn()
        self.draw_legend()
        self.draw_settings()

    def draw_cells(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                rect = pygame.Rect(10 + j * self.cell_size, 10 + i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.get_cell_color(i, j), rect)
                pygame.draw.rect(self.screen, (0, 90, 0), rect, 1)

    def draw_settings(self):
        self.screen.blit(self.setting_background, (800, 210))
        
        slider_positions = {
            'speed': (1128, 293),
            'smart_rabbit': (1128, 391),
            'smart_fox': (1128, 429)
        }
        
        for name, (x, y) in slider_positions.items():
            slider = self.sliders[name]
            slider.draw()
            self.draw_text(str(slider.getValue()), x, y)

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
            text_y = 140  
            lines = self.selected_cell_info.split('- ')
            for line in lines:
                self.draw_text(line, 1005, text_y, font_size=24)
                text_y += 30

    def get_cell_color(self, i, j):
        cell_element = self.grid.cells[i][j].element
        return cell_element.color
    
    def get_slider_value(self, slider_name):
        return self.sliders[slider_name].getValue()


    def draw_text(self, text, x, y, font_size=36):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (139, 69, 19))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        pygame_widgets.update([event])

    def show_widgets(self):
        for widget in self.buttons.values():
            widget.show() 
        for slider in self.sliders.values():
            slider.show()

    def hide_widgets(self):
        for widget in self.buttons.values():
            widget.hide()
        for slider in self.sliders.values():
            slider.hide()