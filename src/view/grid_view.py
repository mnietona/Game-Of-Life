import pygame

class GridView:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.cell_size = 400 // self.grid.size

    def resize(self, new_width, new_height):
        self.cell_size = min(new_width, new_height) // self.grid.size
        
    def render(self):
        self.screen.fill((255, 255, 255))  # Fond blanc

        # Centre grille 
        total_grid_size = self.cell_size * self.grid.size
        margin_x = (self.screen.get_width() - total_grid_size) // 2
        margin_y = (self.screen.get_height() - total_grid_size) // 2

        for i in range(self.grid.size):
            for j in range(self.grid.size):
                rect = pygame.Rect(margin_x + j * self.cell_size, margin_y + i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
