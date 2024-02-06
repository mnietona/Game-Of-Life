import pygame

class GridController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            cell_size = self.view.cell_size
            i = (y - 10) // cell_size
            j = (x - 10) // cell_size
            if 0 <= i < self.model.size and 0 <= j < self.model.size:
                self.view.show_cell_info(i, j)
            pygame.display.flip()  # Mettre à jour l'affichage