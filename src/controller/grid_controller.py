import pygame

class GridController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            i, j = self.get_cell_indices(x, y)
            if self.is_valid_cell(i, j):
                self.view.show_cell_info(i, j)
            
    def get_cell_indices(self, x, y):
        cell_size = self.view.cell_size
        i = (y - 10) // cell_size
        j = (x - 10) // cell_size
        return i, j

    def is_valid_cell(self, i, j):
        return 0 <= i < self.model.size and 0 <= j < self.model.size

    