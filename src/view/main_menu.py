import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.start_button = pygame.Rect(150, 175, 100, 50)  # Position et taille du bouton

    def resize(self, new_width, new_height):
        self.start_button = pygame.Rect(new_width / 2 - 50, new_height / 2 - 25, 100, 50)
                                        
    def render(self):
        self.screen.fill((255, 255, 255))  # Fond blanc
        pygame.draw.rect(self.screen, (0, 0, 0), self.start_button)  # Bouton noir
        font = pygame.font.Font(None, 36)
        text = font.render('Démarrer', True, (255, 255, 255))
        text_rect = text.get_rect(center=self.start_button.center)
        self.screen.blit(text, text_rect)

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.start_button.collidepoint(event.pos):
            return True  # Retourner True si le bouton est cliqué
        return False
