from model.cell import Cell
from model.flora import Carotte

class Grid:
    def __init__(self, size, speed):
        self.size = size
        self.speed = speed
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.tour = 0
        self.update_counter = 0

    def get_cell_info(self, i, j):
        return self.cells[i][j].element.get_info()
    
    def update_systeme(self):
        # Calculez le seuil d'update basé sur la vitesse
        # Par exemple, à speed = 1, update toutes les 10 fois que cette méthode est appelée
        # À speed = 10, update à chaque appel
        seuil_update = 11 - self.speed  # Cela donne un seuil de 1 (pour speed = 10) à 10 (pour speed = 1)

        self.update_counter += 1
        if self.update_counter >= seuil_update:
            self.update_counter = 0  # Réinitialisez le compteur après la mise à jour
            self.tour += 1

            if self.tour % 10 == 0:  # Tous les 10 tours
                self.ajouter_carotte_aleatoirement()
            
            for i in range(self.size):
                for j in range(self.size):
                    self.cells[i][j].update()
        
                
    def ajouter_carotte_aleatoirement(self):
        import random
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        self.cells[i][j].set_element(Carotte(duree_de_vie=50))