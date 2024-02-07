import pygame
from model.cell import Cell

class GridView:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.cell_size = 816 // self.grid.size
        self.selected_cell_info = None
        self.info_box = pygame.Rect(880, 120, 200, 200)
        self.font = pygame.font.Font(None, 24)

    def render(self):
        self.screen.fill((255, 255, 255))  # Fond blanc
        self.draw_cells()
        self.init_info_box()
        if self.selected_cell_info:
            self.redraw_cell_info(*self.selected_cell_info)

    def draw_cells(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                rect = pygame.Rect(10 + j * self.cell_size, 10 + i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

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

    def generate_info_lines(self, i, j, info):
        return [
            f"Cell ({i}, {j})",
            f"Temperature: {info[0]}",
            f"Humidity: {info[1]}",
            # Add other info lines as needed
        ]
