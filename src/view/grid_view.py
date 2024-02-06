import pygame

class GridView:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid

    def render(self):
        self.screen.fill((255, 255, 255))  # Fond blanc
        cell_size = 400 // self.grid.size
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
