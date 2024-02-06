import pygame_widgets
import pygame
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

class MainMenu:
    def __init__(self, screen, on_start):
        self.screen = screen
        self.on_start = on_start
        self.image = pygame.image.load("fond2.png")
        self.image = pygame.transform.scale(self.image, (300, 220))
        self.button = Button(
            screen, 500, 375, 150, 70,
            text='Démarrer',
            fontSize=30, margin=20,
            inactiveColour=(245, 245, 245),
            pressedColour=(255, 255, 255), 
            radius=20,
            onClick=self.on_start,
            image = self.image,
            imageHAlign = 'center'
        )


        
        self.title_font = pygame.font.Font(None, 100)
        self.background_image = pygame.image.load('fond2.jpg')  # Chargez l'image de fond
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))  # Redimensionnez l'image

        self.background2 = pygame.image.load("fond3.png")
        self.background2 = pygame.transform.scale(self.background2,(1450,650))

        self.slider_grid = Slider(self.screen, 500, 550, 200, 15, min=10, max=100, step=10, initial=50)
        self.output_grid = TextBox(self.screen, 760, 545, 40, 40, fontSize=20)
        self.output_grid.disable()
        
        self.slider_temperature = Slider(self.screen, 500, 650, 200, 15, min=-10, max=50, step=5, initial=20)
        self.output_temperature = TextBox(self.screen, 760, 645, 40, 40, fontSize=20)
        self.output_temperature.disable()

    def render(self):
        self.screen.blit(self.background_image, (0, 0))

        self.screen.blit(self.background2, (-150, 430))
        #self.draw_title("Écosystème Pixel")
        #self.draw_texte("La Danse de la Vie", 595, 270, 70)
        self.button.draw()
        self.draw_texte("Taille de la grille", 500, 520, 30)
        self.slider_grid.draw()
        self.output_grid.setText(str(self.slider_grid.getValue()))
        self.output_grid.draw()
        self.draw_texte("Température", 500, 620, 30)
        self.slider_temperature.draw()
        self.output_temperature.setText(str(self.slider_temperature.getValue()))
        self.output_temperature.draw()
        pygame_widgets.update(pygame.event.get())

    def draw_texte(self, text, x, y, size):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        
    def draw_title(self, text):
        text_surface = self.title_font.render(text, True, (254, 254, 254))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, 200))
        self.screen.blit(text_surface, text_rect)
    
    def get_grid_size(self):
        return self.slider_grid.getValue()

    def get_temperature(self):
        return self.slider_temperature.getValue()

    def set_widget_active(self, active):
        if active:
            self.button.show()
            self.slider_grid.show()
            self.output_grid.show()
            self.slider_temperature.show()
            self.output_temperature.show()
        else:
            self.button.hide()
            self.slider_grid.hide()
            self.output_grid.hide()
            self.slider_temperature.hide()
            self.output_temperature.hide()
    