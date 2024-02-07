import pygame
import pygame_widgets
from pygame_widgets.button import Button

class GridView:
    def __init__(self, screen, grid, on_back_to_menu):
        self.screen = screen
        self.grid = grid
        self.on_back_to_menu = on_back_to_menu
        self.cell_size = 816 // self.grid.size
        self.selected_cell_info = None
        self.info_box = pygame.Rect(880, 120, 200, 200)
        self.font = pygame.font.Font(None, 24)
        self.init_ui_elements()


    def init_ui_elements(self):
        self.button = Button(self.screen, 880, 350, 200, 50, text='Retour', fontSize=30, margin=20, onClick=self.on_back_to_menu)
        self.button.hide()
    
    def render(self):
        self.screen.fill((255, 255, 255))  # Fond blanc
        self.draw_cells()
        self.init_info_box()
        if self.selected_cell_info:
            self.redraw_cell_info(*self.selected_cell_info)
        
        pygame_widgets.update(pygame.event.get())
    
    def draw_cells(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                rect = pygame.Rect(10 + j * self.cell_size, 10 + i * self.cell_size, self.cell_size, self.cell_size)
                cell_element = self.grid.cells[i][j].element

                # Choix de la couleur en fonction du type d'élément dans la cellule
                if cell_element.type == "Plant":
                    color = (0, 255, 0)  # Vert pour les plantes
                elif cell_element.type == "Carrot":
                    color = (255, 165, 0)  # Orange pour les carottes
                elif cell_element.type == "Rabbit":
                    color = (128, 128, 128)  # Gris pour les lapins
                else:
                    color = (255, 255, 255)  # Blanc pour les cellules vides

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Contour noir pour chaque cellule


    def init_info_box(self):
        self.screen.fill((220, 220, 220), self.info_box)
        
    def show_cell_info(self, i, j):
        cell = self.grid.cells[i][j]
        self.selected_cell_info = (i, j, cell.info())
        self.redraw_cell_info(i, j, cell.info())

    def redraw_cell_info(self, i, j, info):
        self.init_info_box()
        text_color = (0, 0, 0)
        for line_number, line in enumerate(self.generate_info_lines(i, j, info)):
            text_surface = self.font.render(line, True, text_color)
            self.screen.blit(text_surface, (self.info_box.x + 5, self.info_box.y + 5 + (line_number * 25)))

    
    def set_widget_active(self, active):
        if active:
            self.button.show()
        else:
            self.button.hide()
    
    
    def generate_info_lines(self, i, j, info):
        return [
            f"Cell ({i}, {j})",
            f"Element: {info[0]}"
            ]

