import pygame
import pygame_widgets
from pygame_widgets.button import Button

class GridView:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.cell_size = 816 // grid.size
        self.background_image = self.load_image('assets/background_grid.jpg', screen.get_width(), screen.get_height())
        self.back_clicked = False
        self.pause_play_clicked = False
        self.next_step_clicked = False
        self.init_ui_elements()
        self.hide_widgets()

    def init_ui_elements(self):
        self.button_back = Button(self.screen, 900, 350, 200, 50, fontSize=30, margin=20,
                                  image=self.load_image("assets/retour.png", 320, 230),
                                  onClick=self.set_back_clicked)

        self.button_pause_play = Button(self.screen, 1025, 40, 80, 48, fontSize=30, margin=20,
                                        image=self.load_image("assets/Pause.png", 160, 160),
                                        onClick=self.set_pause_play_clicked)

        self.button_next_step = Button(self.screen, 1115, 40, 80, 48, fontSize=30, margin=20,
                                       image=self.load_image("assets/Next.png", 160, 160),
                                       onClick=self.set_next_step_clicked)

    def set_back_clicked(self):
        self.back_clicked = True

    def set_pause_play_clicked(self):
        self.pause_play_clicked = True

    def set_next_step_clicked(self):
        self.next_step_clicked = True

    def reset_button_clicks(self):
        self.back_clicked = False
        self.pause_play_clicked = False
        self.next_step_clicked = False

    def load_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_cells()
        pygame_widgets.update(pygame.event.get())

    def draw_cells(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                rect = pygame.Rect(10 + j * self.cell_size, 10 + i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.get_cell_color(i, j), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Contour noir pour chaque cellule

    def get_cell_color(self, i, j):
        # Cette méthode devrait retourner la couleur de la cellule basée sur son état
        # Exemple simplifié:
       
        return (255, 255, 255)  # Blanc pour les cellules mortes

    def redraw_cell_info(self, i, j, info):
        # Affiche les informations sur la cellule sélectionnée
        # Cette méthode doit être implémentée en fonction de la structure de vos données
        pass

    def draw_text(self, text, x, y, font):
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))
    
    def handle_event(self, event):
        pygame_widgets.update([event])
    
    def show_widgets(self):
        self.button_back.show()
        self.button_pause_play.show()
        self.button_next_step.show()

    def hide_widgets(self):
        self.button_back.hide()
        self.button_pause_play.hide()
        self.button_next_step.hide()

    
