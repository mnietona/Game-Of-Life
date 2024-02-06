import pygame
from view.slider import Slider

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.start_button = pygame.Rect(500, 375, 150, 70)  # Position et taille du bouton

        # Définir les polices
        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 36)

        # Couleurs
        self.background_color = (255, 218, 185)
        self.button_color = (105, 105, 105)
        self.text_color = (255, 255, 255)  # Blanc
        
        # Curseurs
        self.grid_size_slider = Slider(screen, 500, 500, 10, 100, initial_value=50)
        self.temperature_slider = Slider(screen, 500, 600, -10, 50, initial_value=20)


    def render(self):
        self.screen.fill(self.background_color)
        self.draw_title("Game Of The Live")
        self.draw_rounded_button("Démarrer", self.start_button, self.button_color)
        self.grid_size_slider.draw()
        self.temperature_slider.draw()

    def draw_title(self, text):
        text_surface = self.title_font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, 300))
        self.screen.blit(text_surface, text_rect)

    def draw_rounded_button(self, text, rect, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        text_surface = self.button_font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                return True  # Retourner True si le bouton est cliqué
            
            self.grid_size_slider.handle_event(event)
            self.temperature_slider.handle_event(event)
        return False
    
