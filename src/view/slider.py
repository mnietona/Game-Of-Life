import pygame

# A REPARER FONCTIONNE PAS
class Slider:
    def __init__(self, screen, x, y, min_value, max_value, initial_value=0):
        self.screen = screen
        self.x = x
        self.y = y
        self.min = min_value
        self.max = max_value
        self.value = initial_value
        self.slider_rect = pygame.Rect(x, y, 200, 10)  # Taille du slider
        self.handle_rect = pygame.Rect(x + (200 * (initial_value - min_value) / (max_value - min_value)), y, 10, 10)
        
        # Configuration de la police pour afficher la valeur
        self.font = pygame.font.Font(None, 24)

    def draw(self):
        # Dessiner le slider
        pygame.draw.rect(self.screen, (180, 180, 180), self.slider_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.handle_rect)

        # Dessiner la valeur du slider
        value_text = self.font.render(str(self.get_value()), True, (0, 0, 0))
        text_rect = value_text.get_rect(center=(self.handle_rect.x + 20, self.handle_rect.y - 20))
        self.screen.blit(value_text, text_rect)

    def handle_event(self, event):
       self.value = 30
       
    def get_value(self):
        return self.value
