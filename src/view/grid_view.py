import pygame
import pygame_widgets
from pygame_widgets.button import Button

class GridView:
    def __init__(self, screen, grid, on_back_to_menu, controller = None):
        self.controller = controller
        self.screen = screen
        self.grid = grid
        self.on_back_to_menu = on_back_to_menu
        self.cell_size = 816 // self.grid.size
        self.selected_cell_info = None
        self.info_box = pygame.Rect(880, 120, 200, 200)
        self.font = pygame.font.Font(None, 24)
        self.background_image = self.load_image('images/background4.jpg', screen.get_width(), screen.get_height())
        self.init_ui_elements()

    def set_controller(self, controller):
        self.controller = controller

    def init_ui_elements(self):
        self.button_back = Button(self.screen, 900, 350, 200, 50, text='', fontSize=30, margin=20,
                                  image =self.load_image("images/retour.png",320,230) ,onClick=self.on_back_to_menu)
        self.button_back.hide()
        
        self.button_pause = Button(self.screen, 830, 450, 100, 60, fontSize=30, margin=20,
                                   inactiveColour=(245, 245, 245), pressedColour=(255, 255, 255),
                                   radius=20, image = self.load_image("images/Pause.png",200,200),
                                   onClick=self.on_pause)
        
        self.button_play = Button(self.screen, 830, 450, 100, 60, fontSize=30, margin=20,
                                   inactiveColour=(255, 255, 255), pressedColour=(255, 255, 255),
                                   radius=20, image = self.load_image("images/Play.png",200,200),
                                  onClick=self.on_pause)

        self.button_previous_step = Button(self.screen, 950, 450, 100, 60, fontSize=30, margin=20,
                                   inactiveColour=(255, 255, 255), pressedColour=(255, 255, 255),
                                   radius=20, image = self.load_image("images/Previous.png",200,200),
                                  onClick= None)

        self.button_next_step = Button(self.screen, 1070, 450, 100, 60, fontSize=30, margin=20,
                                   inactiveColour=(255, 255, 255), pressedColour=(255, 255, 255),
                                   radius=20, image = self.load_image("images/Next.png",200,200),
                                  onClick= None)
        self.button_pause.hide()
   
    def on_pause(self):
        self.controller.is_paused = not self.controller.is_paused
        self.switch_pause_button()

    def switch_pause_button(self):
        if self.controller.is_paused:
            self.button_pause.hide()
            self.button_play.show()
        else:
            self.button_play.hide()
            self.button_pause.show()

    def load_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))
        
    
    def render(self):
        #self.screen.fill((255, 255, 255))  # Fond blanc
        self.screen.blit(self.background_image, (0, 0))
        self.draw_cells()
        self.init_info_box()
    
        #self.draw_text(str(self.grid.update_count // self.grid.speed ), 685, 605, self.font) timer
        if self.selected_cell_info:
            self.redraw_cell_info(*self.selected_cell_info)
        
        pygame_widgets.update(pygame.event.get())
    
    def draw_text(self, text, x, y, font):
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))
    
    def draw_cells(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                rect = pygame.Rect(10 + j * self.cell_size, 10 + i * self.cell_size, self.cell_size, self.cell_size)
                cell_element = self.grid.cells[i][j].element

                # Choix de la couleur en fonction du type d'élément dans la cellule
                match cell_element.type:
                    case "Plant":
                        color = (58, 137, 35)  # Vert pour les plantes
                    case "Carrot":
                        color = (255, 165, 0)  # Orange pour les carottes
                    case "Rabbit":
                        color = (253, 241, 184) # Gris pour les lapins
                    case "Fox":
                        color = (255, 0, 0) # Rouge pour les renards
                    case _:
                        color = (255, 255, 255)  # Blanc pour les cellules vides

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Contour noir pour chaque cellule


    def init_info_box(self):
        self.fond_info = self.load_image("images/info_box_bg.png",650,600)
        self.screen.blit(self.fond_info, (680,-120))
        
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

    
    def set_widget_active(self, active):
        if active:
            self.button_back.show()
            self.button_pause.show()
            self.button_previous_step.show()
            self.button_next_step.show()
        else:
            self.button_back.hide()
            self.button_pause.hide()
            self.button_play.hide()
            self.button_previous_step.hide()
            self.button_next_step.hide()
    
    
    def generate_info_lines(self, i, j, info):
        return [
            f"Cell ({i}, {j})",
            f"Element: {info[0]}"
            ]
