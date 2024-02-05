import pygame
import sys

class MouseHandler:
    def __init__(self):
        self.clicked = False
        self.position = (0, 0)

    def update(self):
        self.clicked = False  # Réinitialiser l'état du clic à chaque mise à jour
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True
                self.position = pygame.mouse.get_pos()


class Rectangle:
    def __init__(self,pos_x,pos_y,size_x,size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
    

        self.background_color =  (0,0,0) # Couleur d'arrière-plan
        self.content_color =  (128, 128, 128) # Couleur du contenu

    def draw(self, screen):
        
        pygame.draw.rect(screen, self.background_color, (self.pos_x, self.pos_y, self.size_x, self.size_y))

        
        content_size_x = self.size_x - 2 
        content_size_y = self.size_y - 2 
        content_rect = pygame.Rect(self.pos_x + 1, self.pos_y + 1, content_size_x, content_size_y)
        pygame.draw.rect(screen, self.content_color, content_rect) 

class InfoBox(Rectangle):
    def __init__(self, pos_x, pos_y, size_x,size_y):
        super().__init__(pos_x, pos_y,size_x,size_y)
        self.text = ""  # Texte à afficher dans la cellule
        self.font = pygame.font.Font(None, 24)

    def draw(self,screen):
        super().draw(screen)
        text_surface = self.font.render(self.text, True, (0, 0, 0))  # Texte en noir
        text_rect = text_surface.get_rect(center=(self.pos_x + self.size_x // 2, self.pos_y + self.size_y // 2))
        screen.blit(text_surface, text_rect)

    def set_text(self, new_text):
        self.text = new_text
        
    ...


class Cell(Rectangle):
    def __init__(self, row, col, size_x,size_y):
        x = col * size_x
        y = row * size_y
        super().__init__(x,y,size_x,size_y)
        self.image = None  # Remplacez "your_image.png" par le chemin de votre image
        self.climat = None
        self.animal = None

    def draw(self, screen):
        super().draw(screen)
        if self.image != None:
            screen.blit(self.image, (self.pos_x, self.pos_y))

    def setImage(self,animal_file):
        self.image = pygame.image.load(animal_file)  # Remplacez "your_image.png" par le chemin de votre image
        self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))  # Redimensionner l'image

    def defineClimat(self, climat):
        self.climat = climat
        if climat == "plaine":
            self.content_color = (144, 238, 144)
        elif climat == "foret":
            self.content_color =  (0, 128, 0) 
        elif climat == "ocean":
            self.content_color = (0, 0, 255)
        elif climat == "desert":
            self.content_color = (245, 245, 220)
        ...

    def removeAnimal(self):
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)

    def defineAnimal(self, animal):
        self.animal = animal
        if animal == "renard":
            self.setImage("src/gui/img/renard.png")
        elif animal == "lapin":
            self.setImage("src/gui/img/lapin.png")
        elif animal == "empty":
            self.removeAnimal()
            self.animal = None

        ...

    def get_info(self):
        if self.animal != None and self.climat != None:
            return f"Un {self.animal} dans un biome {self.climat}"
        elif self.animal == None and self.climat != None:
            return f"Le biome {self.climat}"
        else:
            return "il ya r"
        
class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.cells = [[Cell(row, col, cell_size,cell_size) for col in range(cols)] for row in range(rows)]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].draw(screen)
    #au lieu de faire case par case, matrice ?            
    def setClimat(self,x,y,climat):   
        self.cells[x][y].defineClimat(climat)

    def setAnimal(self,x,y,animal):
        self.cells[x][y].defineAnimal(animal)

    def getCellInfo(self,x,y):
        return self.cells[x][y].get_info()
    
    def initialiseMap(self, matrice):
        """
        prendre une matrice de 100 x 100 d'information et transforme directement 
        """
        ...
    

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Grille de cases 100x100")
        self.mouse_handler = MouseHandler()

    def fill_background(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.flip()

#pour test     
def testShowCell(grid):
    grid.setClimat(13,12,"ocean")
    grid.setClimat(1,1,"foret")
    grid.setClimat(44,82,"desert")
    grid.setClimat(5,5,"desert")
    grid.setClimat(16,77,"plaine")
    grid.setClimat(32,42,"plaine")

    grid.setAnimal(90,11,"lapin")
    grid.setAnimal(80,21,"lapin")
    grid.setAnimal(44,82,"lapin")
    grid.setAnimal(1,22,"renard")
    grid.setAnimal(44,11,"renard")
    grid.setAnimal(77,46,"renard")

    grid.setAnimal(1,1,"lapin")
    grid.setAnimal(1,1,"empty")


def main():
    pygame.init()

    # Paramètres de la grille
    grid_size = 100
    cell_size = 13  # Ajustez la taille de la cellule selon vos besoins

    # Création de l'écran, de la grille et initialisation de Pygame
    screen = Screen(1800,1300)
    grid = Grid(grid_size, grid_size, cell_size)

    info_box = InfoBox(1325,20,450,50)

    # Couleur de fond de l'écran (gris)
    background_color = (128, 128, 128)

    # Boucle principale
    while True:
        screen.mouse_handler.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if screen.mouse_handler.clicked:
            
            info_box.set_text("")
            # Clic de souris détecté, faites quelque chose avec screen.mouse_handler.position
            mouse_x, mouse_y = screen.mouse_handler.position
            col = mouse_x // cell_size
            row = mouse_y // cell_size
            info_box.set_text(grid.getCellInfo(row,col))

           

        # Changer la couleur de fond de l'écran
        screen.fill_background(background_color)

        # Dessiner la grille de cases
        grid.draw(screen.screen)

        testShowCell(grid)

        info_box.draw(screen.screen)
        

        # Mettre à jour l'affichage
        screen.update()

if __name__ == "__main__":
    main()