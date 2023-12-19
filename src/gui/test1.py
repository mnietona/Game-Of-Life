import pygame
import sys



class Rectangle:
    def __init__(self,row,col,size):
        self.row = row
        self.col = col
        self.size = size

        self.x = self.col * self.size
        self.y = self.row * self.size

        self.background_color =  (0,0,0) # Couleur d'arrière-plan
        self.content_color =  (128, 128, 128) # Couleur du contenu

    def draw(self, screen):
        
        pygame.draw.rect(screen, self.background_color, (self.x, self.y, self.size, self.size))

        # Dessiner la couleur du contenu (rectangle plus petit à l'intérieur)
        content_size = self.size - 2  # Ajustez selon vos préférences
        content_rect = pygame.Rect(self.x + 1, self.y + 1, content_size, content_size)
        pygame.draw.rect(screen, self.content_color, content_rect)     


class Cell(Rectangle):
    def __init__(self, row, col, size):
        super().__init__(row,col,size)
        self.image = None  # Remplacez "your_image.png" par le chemin de votre image
        

    def draw(self, screen):
        super().draw(screen)
        if self.image != None:
            screen.blit(self.image, (self.x, self.y))

    def setImage(self,animal_file):
        self.image = pygame.image.load(animal_file)  # Remplacez "your_image.png" par le chemin de votre image
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # Redimensionner l'image

    def defineClimat(self, climat):
        if climat == "plaine":
            self.content_color = (144, 238, 144)
        elif climat == "foret":
            self.content_color =  (0, 128, 0) 
        elif climat == "ocean":
            self.content_color = (0, 0, 255)
        elif climat == "desert":
            self.content_color = (245, 245, 220)
        ...

    def defineAnimal(self, animal):
        if animal == "renard":
            self.setImage("renard.png")
        elif animal == "lapin":
            self.setImage("lapin.png")

   

class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.cells = [[Cell(row, col, cell_size) for col in range(cols)] for row in range(rows)]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].draw(screen)
    #au lieu de faire case par case, matrice ?            
    def setClimat(self,x,y,climat):   
        self.cells[x][y].defineClimat(climat)

    def setAnimal(self,x,y,animal):
        self.cells[x][y].defineAnimal(animal)
    

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Grille de cases 100x100")

    def fill_background(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.flip()

def main():
    pygame.init()

    # Paramètres de la grille
    grid_size = 100
    cell_size = 13  # Ajustez la taille de la cellule selon vos besoins

    # Création de l'écran, de la grille et initialisation de Pygame
    screen = Screen(1800,1300)
    grid = Grid(grid_size, grid_size, cell_size)

    # Couleur de fond de l'écran (gris)
    background_color = (128, 128, 128)

    # Boucle principale
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Changer la couleur de fond de l'écran
        screen.fill_background(background_color)

        # Dessiner la grille de cases
        grid.draw(screen.screen)

        grid.setClimat(13,12,"ocean")
        grid.setClimat(1,12,"foret")
        grid.setClimat(44,82,"desert")
        grid.setClimat(16,77,"plaine")
        grid.setClimat(32,42,"plaine")

        grid.setAnimal(90,11,"lapin")
        grid.setAnimal(80,21,"lapin")
        grid.setAnimal(86,54,"lapin")
        grid.setAnimal(1,22,"renard")
        grid.setAnimal(44,11,"renard")
        grid.setAnimal(77,46,"renard")

        # Mettre à jour l'affichage
        screen.update()

if __name__ == "__main__":
    main()