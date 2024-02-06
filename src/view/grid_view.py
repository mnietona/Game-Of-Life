import pygame
from model.cell import Cell

class GridView:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.cell_size = 816 // self.grid.size
        self.selected_cell_info = None  # Attribut pour mémoriser les informations de la cellule sélectionnée
    
    def init_info_box(self):
        # Initialiser la boîte d'informations vide
        # METTRE TITRE ET MIEUX CONFIGURER TAILLE ET COULEUR 
        self.info_box = pygame.Rect(880, 120, 200, 200)
        self.screen.fill((220, 220, 220), self.info_box)
        
    def render(self):
        self.screen.fill((255, 255, 255))  # Fond blanc

        for i in range(self.grid.size):
            for j in range(self.grid.size):
                rect = pygame.Rect(10 + j * self.cell_size, 10 + i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        
        self.init_info_box()
        # Redessiner les informations de la cellule sélectionnée, si disponible
        if self.selected_cell_info:
            self.redraw_cell_info(*self.selected_cell_info)
    
    def show_cell_info(self, i, j):
        cell = self.grid.cells[i][j]
        self.selected_cell_info = (i, j, cell.info())  # Mémoriser les informations de la cellule
        self.redraw_cell_info(i, j, cell.info())
    
    def redraw_cell_info(self, i, j, info):
        # Redessiner la boîte d'informations avec les informations de la cellule
        self.screen.fill((220, 220, 220), self.info_box)

        # Configurer la police et la couleur du texte
        font = pygame.font.Font(None, 24)
        text_color = (0, 0, 0)

        # Créer et afficher les lignes de texte
        info_lines = [
            f"Cell ({i}, {j})",
            f"Temperature: {info[0]}",
            f"Humidity: {info[1]}",
            f"Vegetation: {info[2]}",
            f"Elevation: {info[3]}",
            f"Is water: {info[4]}"
        ]

        for line_number, line in enumerate(info_lines):
            text_surface = font.render(line, True, text_color)
            self.screen.blit(text_surface, (self.info_box.x + 5, self.info_box.y + 5 + (line_number * 25)))