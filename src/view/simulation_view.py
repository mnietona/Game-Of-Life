import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from constants import *
import matplotlib.pyplot as plt

class SimulationView:
    def __init__(self, screen, grid, model):
        self.screen = screen
        self.model = model
        self.grid = grid    
        self.grid_size = 800
        self.cell_size = self.grid_size // self.grid.size
        self.load_background_images()
        self.init_values()
        self.reset_click_states()
        self.init_ui_elements()
        self.hide_widgets()
        
    def init_values(self):
        self.selected_cell = None  
        self.selected_cell_info = ""
        self.turn = 0
        self.count_rabbit = 0
        self.count_fox = 0
        self.count_carrot = 0
        
        # Pour le graphique
        self.rabbit_population = []
        self.fox_population = []
        self.carrot_population = []
        self.turns = []
        self.graph_figure = None
        self.graph_axes = None

    def calculate_ratios(self):
        current_width, current_height = self.screen.get_size()
        return current_width / SCREEN_WIDTH, current_height / SCREEN_HEIGHT
    
    def load_background_images(self):
        width_ratio, height_ratio = self.calculate_ratios()
        self.background_image = self.load_image('assets/background_grid.jpg', self.screen.get_width(), self.screen.get_height())
        self.turn_background = self.load_image("assets/tour.png", 310 * width_ratio, 140 * height_ratio)
        self.info_box_background = self.load_image("assets/info_box.png", 330 * width_ratio, 365 * height_ratio)
        self.setting_background = self.load_image("assets/settings.png", 380 * width_ratio, 280 * height_ratio)
        self.legend_background = self.load_image("assets/legende.png", 330 * width_ratio, 280 * height_ratio)

    def init_ui_elements(self):
        width_ratio, height_ratio = self.calculate_ratios()
        
        taille_x, taille_y = int(70 * width_ratio), int(70 * height_ratio)
        self.buttons = {
            'back': self.create_button(int(1050 * width_ratio), int(750 * height_ratio), 150, 40, "assets/return.png", self.toggle_click_state, 'back_clicked', 200, 100),
            'generate_graph': self.create_button(int(850 * width_ratio), int(750 * height_ratio), 150, 40, "assets/return.png", self.toggle_click_state, 'graph_clicked', 200, 100),
            'play': self.create_button(int(1190 * width_ratio), int(110 * height_ratio), taille_x, taille_y, "assets/play.png", self.toggle_pause_play),
            'pause': self.create_button(int(1190 * width_ratio), int(110 * height_ratio), taille_x, taille_y, "assets/pause.png", self.toggle_pause_play),
            'next_step': self.create_button(int(1300 * width_ratio), int(110 * height_ratio), taille_x, taille_y, "assets/next.png", self.toggle_click_state, 'next_step_clicked')
        }
        
        taille_x, taille_y = int(160 * width_ratio), int(15 * height_ratio)
        self.sliders = {
            'speed': self.create_slider(int(920 * width_ratio), int(254 * height_ratio), taille_x, taille_y, 1, 10, 1, self.model.speed),
            'carrot_spawn_speed': self.create_slider(int(920 * width_ratio), int(287 * height_ratio), taille_x, taille_y, 1, 10, 1, self.model.carrot_spawn_speed),
            'smart_rabbit': self.create_slider(int(920 * width_ratio), int(362 * height_ratio), taille_x, taille_y, 1, 3, 1, self.model.smart_level_rabbit),
            'smart_fox': self.create_slider(int(920 * width_ratio), int(400 * height_ratio), taille_x, taille_y, 1, 3, 1, self.model.smart_level_fox)
        }

    def create_button(self, x, y, taille_x, taille_y, image_path, onclick_function, click_state=None, path_taille_x=120, path_taille_y=110):
        image = self.load_image(image_path, path_taille_x, path_taille_y)
        if click_state is not None:
            return Button(self.screen, x, y, taille_x, taille_y, inactiveColour=(245, 245, 245), pressedColour=(245, 245, 245),hoverColour=(245, 245, 245), image=image, onClick=lambda: onclick_function(click_state), radius=90)
        else:
            return Button(self.screen, x, y, taille_x, taille_y, inactiveColour=(245, 245, 245), pressedColour=(245, 245, 245),hoverColour=(245, 245, 245), image=image, onClick=onclick_function, radius=90)

    def create_slider(self, x, y, taille_x, taille_y, min_val, max_val, step, initial):
        return Slider(self.screen, x, y, taille_x, taille_y, min=min_val, max=max_val, step=step, initial=initial,
                      colour=(245,245,220), handleColour=(222,184,135))
        
    def load_image(self, path, width, height):
        return pygame.transform.scale(pygame.image.load(path), (width, height))

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        #self.draw_grid() pour debeug jour J
        self.draw_cells()
        self.draw_widgets()
        pygame_widgets.update(pygame.event.get())

    def draw_widgets(self):
        width_ratio, height_ratio = self.calculate_ratios()
        self.draw_turn(width_ratio, height_ratio)
        self.draw_info_box(width_ratio, height_ratio)
        self.draw_settings(width_ratio, height_ratio)
        self.draw_legend(width_ratio, height_ratio)
        self.draw_graph(width_ratio, height_ratio)
        
    def draw_grid(self):
        width_ratio, height_ratio = self.calculate_ratios()
        square_rect = pygame.Rect((10,10), (800 * width_ratio, 800 * height_ratio))
        pygame.draw.rect(self.screen, (0, 90, 0), square_rect)
        
    def draw_cells(self):
        width_ratio, height_ratio = self.calculate_ratios()
        
        cell_size = self.grid_size / self.grid.size
        
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                cell_x = (10 + j * cell_size) * width_ratio
                cell_y = (10 + i * cell_size) * height_ratio
                cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
                pygame.draw.rect(self.screen, self.get_cell_color(i, j), cell_rect, width =0)
                pygame.draw.rect(self.screen, (0, 90, 0), cell_rect, 1)

    def draw_settings(self, width_ratio, height_ratio):
        self.screen.blit(self.setting_background, (790 * width_ratio, 190 * height_ratio))
        
        slider_positions = {
            'speed': (1107 * width_ratio, 260 * height_ratio),
            'carrot_spawn_speed': (1106 * width_ratio, 293 * height_ratio),
            'smart_rabbit': (1104 * width_ratio, 368 * height_ratio),
            'smart_fox': (1104 * width_ratio, 406 * height_ratio)
        }
        
        for name, (x, y) in slider_positions.items():
            slider = self.sliders[name]
            slider.draw()
            self.draw_text(str(slider.getValue()), x, y, font_size=int(36 * height_ratio))

    def draw_legend(self, width_ratio, height_ratio):
        self.screen.blit(self.legend_background, (1110 * width_ratio, 190 * height_ratio))
        
        self.draw_text(f"{self.count_carrot}", 1274 * width_ratio, 250 * height_ratio, font_size=int(36 * height_ratio))
        self.draw_text(f"{self.count_rabbit}", 1274 * width_ratio, 330 * height_ratio, font_size=int(36 * height_ratio))
        self.draw_text(f"{self.count_fox}", 1274 * width_ratio, 405 * height_ratio, font_size=int(36 * height_ratio))
    
    def draw_turn(self, width_ratio, height_ratio):
        self.screen.blit(self.turn_background, (1120 * width_ratio, -22 * height_ratio))
        self.draw_text(f"{self.turn}", 1275 * width_ratio , 70 * height_ratio, font_size=int(36 * height_ratio))

    def draw_info_box(self, width_ratio, height_ratio):
        self.screen.blit(self.info_box_background, (820 * width_ratio, -90 * height_ratio))
        
        if self.selected_cell:
            text_y = 65 * height_ratio  
            lines = self.selected_cell_info.split('- ')
            for line in lines:
                self.draw_text(line, 983 * width_ratio, text_y, font_size=int(30 * height_ratio))
                text_y += 25 * height_ratio
    
    def draw_graph_axes(self, graph_surface):
        _, graph_height = graph_surface.get_size()
        pygame.draw.line(graph_surface, BLACK, (40, 0), (40, graph_height), 2)
        tick_length = 5  
        num_ticks = 5 
        tick_interval = graph_height / num_ticks 
        for i in range(num_ticks + 1):
            y = i * tick_interval
            pygame.draw.line(graph_surface, BLACK, (40 - tick_length / 2, y), (40 + tick_length / 2, y), 2)
        font = pygame.font.Font(None, 18)
        label_y = font.render('Population', True, BLACK)
        graph_surface.blit(label_y, (10, 5))
        
    def draw_graph(self, width_ratio, height_ratio):
        graph_width = 570 * width_ratio
        graph_height = 250 * height_ratio
        graph_origin = (835 * width_ratio, 470 * height_ratio)
        
        graph_surface = pygame.Surface((graph_width, graph_height))
        graph_surface.fill((255, 167, 109))

        self.draw_graph_axes(graph_surface)
        
        max_turns = 50  
        scale_x = graph_width / max_turns
        scale_y = graph_height / max(250, max(self.rabbit_population + self.fox_population + self.carrot_population))


        start_index = max(0, len(self.turns) - max_turns)

        rabbit_points = [(i * scale_x + 40, graph_height - 40 - val * scale_y) for i, val in enumerate(self.rabbit_population[start_index:])]
        fox_points = [(i * scale_x + 40, graph_height - 40 - val * scale_y) for i, val in enumerate(self.fox_population[start_index:])]
        carrot_points = [(i * scale_x + 40, graph_height - 40 - val * scale_y) for i, val in enumerate(self.carrot_population[start_index:])]

        if len(rabbit_points) > 1:
            pygame.draw.lines(graph_surface, WHITE, False, rabbit_points, 2)
        if len(fox_points) > 1:
            pygame.draw.lines(graph_surface, RED, False, fox_points, 2)
        if len(carrot_points) > 1:
            pygame.draw.lines(graph_surface, ORANGE_GRAPH, False, carrot_points, 2)
        
        self.screen.blit(graph_surface, graph_origin)
    
    def draw_text(self, text, x, y, font_size=36):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (139, 69, 19))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def update_data_and_graph(self, turn, rabbits, foxes, carrot):
        self.turns.append(turn)
        self.rabbit_population.append(rabbits)
        self.fox_population.append(foxes)
        self.carrot_population.append(carrot)

    def toggle_click_state(self, state):
        setattr(self, state, not getattr(self, state))

    def toggle_pause_play(self):
        self.pause_play_clicked = not self.pause_play_clicked
        self.update_buttons_based_on_pause_state(self.pause_play_clicked)
    
    def update_buttons_based_on_pause_state(self, is_paused):
        self.buttons['play'].show() if is_paused else self.buttons['pause'].show()
        self.buttons['pause'].hide() if is_paused else self.buttons['play'].hide()

    def get_cell_color(self, i, j):
        cell_element = self.grid.cells[i][j].element
        return cell_element.color
    
    def get_slider_value(self, slider_name):
        return self.sliders[slider_name].getValue()

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
    
    def reset_click_states(self):
        self.back_clicked = False
        self.pause_play_clicked = False
        self.next_step_clicked = False
        self.graph_clicked=False
    
    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.load_background_images()
        self.init_ui_elements()
    
    def generate_graph(self):
        plt.figure(figsize=(12, 6))

        # Plot the rabbit and fox populations over time with enhanced styling
        plt.plot(self.turns, self.rabbit_population, label='Rabbits', linewidth=2, linestyle='-', marker='o', markersize=5)
        plt.plot(self.turns, self.fox_population, label='Foxes', linewidth=2, linestyle='--', marker='x', markersize=5)
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.title('Population Dynamics Over Time')
        plt.legend()

        plt.grid(True)  # Add gridlines

        plt.tight_layout()

        plt.show()
        plt.close()
