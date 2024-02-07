import random
from model.cell import Cell
from src.model.flora import Carrot
from model.rabbit import Rabbit
from model.fox import Fox

class Grid:
    def __init__(self, size, speed):
        self.size = size
        self.speed = speed
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.update_count = 0
        self.init_grid()
        
    def init_grid(self):
        # 5 lapin aléatoire
        for _ in range(5):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.cells[x][y].set_element(Rabbit())
        
        
    def update_systeme(self):
        self.update_count += 1

        # Créer une copie pour éviter de modifier la liste pendant son itération
        rabbits = [(i, j) for i in range(self.size) for j in range(self.size) if isinstance(self.cells[i][j].element, Rabbit)]

        for i, j in rabbits:
            rabbit = self.cells[i][j].element
            rabbit.update(self, i, j)

        # Logique renards...

        # Si on augmente la muliplication du denominateur on diminue la fréquence d'apparition des carottes
        if self.update_count % ((self.size // self.speed) * 1 ) == 0: 
            self.spawn_carrot()

    def spawn_carrot(self):
        potential_locations = []
        for i in range(self.size):
            for j in range(self.size):
                if self.is_safe_for_carrot(i, j):
                    potential_locations.append((i, j))
                    break

        if potential_locations:
            x, y = random.choice(potential_locations)
            self.cells[x][y].set_element(Carrot())


    def is_safe_for_carrot(self, i, j):
        # Vérifier si la cellule actuelle ou les cellules adjacentes contiennent de la faune
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= i + dx < self.size and 0 <= j + dy < self.size:
                    if isinstance(self.cells[i + dx][j + dy].element, (Rabbit, Fox)):
                        return False
        return True
