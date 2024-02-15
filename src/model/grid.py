import random
from model.cell import Cell
from model.flora import Carrot, Plant
from model.rabbit import Rabbit

class Grid:
    def __init__(self, size, speed):
        self.size = size
        self.speed = speed
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.turn = 0
        self.update_counter = 0
        self.entity_positions = {}
        self.init_grid()

    def get_cell_info(self, i, j):
        return self.cells[i][j].element.get_info()
    
    def init_grid(self):
        # Ajouter des lapins
        for _ in range(5):
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)
            rabbit = Rabbit(50, 5, self)
            self.cells[i][j].set_element(rabbit)
            self.entity_positions[(i, j)] = rabbit    
    
    def update_systeme(self, force_update=False):
        if force_update or self.update_counter >= (11 - self.speed):
            self.update_counter = 0  # Réinitialiser le compteur après la mise à jour
            self.turn += 1

            positions_to_update = list(self.entity_positions.keys())
            for position in positions_to_update:
                i, j = position
                if position in self.entity_positions:
                    self.cells[i][j].update(i, j, self)
            
            if self.turn % 10 == 0:  
                self.add_carrot()
        else:
            self.update_counter += 1  
        
    def remove_element(self, i, j):
        self.cells[i][j].set_element(Plant())
        self.entity_positions.pop((i, j), None)
    
    def is_cell_valid(self, i, j):
        return isinstance(self.cells[i][j].element, Plant)
        
    def add_carrot(self):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        if self.is_cell_valid(i, j):
            carrot = Carrot(lifespan=50)
            self.cells[i][j].set_element(carrot)
            self.entity_positions[(i, j)] = carrot
        else:
            self.add_carrot()
    
    def update_entity_position(self, old_position, new_position):
        entity = self.entity_positions.pop(old_position, None)
        if entity:
            self.entity_positions[new_position] = entity
            # Assurez-vous que la cellule à l'ancienne position est maintenant vide ou a une nouvelle plante
            self.cells[old_position[0]][old_position[1]].set_element(Plant())
            # Mettez à jour l'élément dans la nouvelle position
            self.cells[new_position[0]][new_position[1]].set_element(entity)
    