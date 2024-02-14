import random
from model.cell import Cell
from model.flora import Carrot
from model.rabbit import Rabbit
from model.fox import Fox

class Grid:
    def __init__(self, size, speed, rabbit_number, fox_number):
        self.size = size
        self.speed = speed
        self.rabbit_count = rabbit_number
        self.carrot_count = 0
        self.fox_count = fox_number
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.update_count = 0
        self.init_grid()
        self.max_rabbits = 15
        #max carrot et max fox à ajouter pr les tests (pr l'instant maxrabbit est utilité pr tout)

    def init_grid(self):
        occupied_positions = set()

        # Placer un nombre de lapins choisit par l'utilisateur
        for _ in range(self.rabbit_count):
            x, y = self.get_random_free_position(occupied_positions)
            self.cells[x][y].set_element(Rabbit())
            occupied_positions.add((x, y))
            #self.rabbit_count += 1
        # Place un nombre de renards choisit par l'utilisateur
        for _ in range(self.fox_count):
            x, y = self.get_random_free_position(occupied_positions)
            self.cells[x][y].set_element(Fox())
            occupied_positions.add((x, y))

    def get_random_free_position(self, occupied_positions):
        x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        while (x, y) in occupied_positions:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        return x, y
    def update_systeme(self):
        print('rabbit count : ', self.rabbit_count)
        self.update_count += 1

        # Mise à jour des lapins et des renards
        for i in range(self.size):
            for j in range(self.size):
                element = self.cells[i][j].element
                if isinstance(element, Rabbit):
                    element.update(self, i, j)
                elif isinstance(element, Fox):
                    element.update(self, i, j)

        if self.update_count % ((self.size // self.speed)) == 0:
            if self.carrot_count <= self.max_rabbits:
              self.spawn_carrot()
              self.carrot_count += 1 # décommenté pr une question de clareté mais vous pouvez remettre si vous voulez
    def spawn_carrot(self):
        potential_locations = []
        for i in range(self.size):
            for j in range(self.size):
                if self.is_safe_for_carrot(i, j):
                    potential_locations.append((i, j))


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
