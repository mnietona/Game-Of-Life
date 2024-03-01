import random
from constants import MOVES
from model.cell import Cell
from model.flora import Carrot, Plant
from model.rabbit import Rabbit
from model.fox import Fox

class Grid:
    def __init__(self, size):
        self.size = size
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.entity_positions = {}

    def add_entity(self, i, j, entity_class):
        kwargs = {}
        if entity_class != Carrot:
            kwargs['grid_size'] = self.size
        entity = entity_class(**kwargs)
        self.cells[i][j].set_element(entity)
        self.entity_positions[(i, j)] = entity

    def remove_element(self, i, j):
        if (i, j) in self.entity_positions:
            del self.entity_positions[(i, j)]
            self.cells[i][j].set_element(Plant())
            
    def is_cell_valid(self, i, j):
        if not (0 <= i < self.size and 0 <= j < self.size):
            return False 
        cell_content = self.cells[i][j].element
        return isinstance(cell_content, Plant) 
        
    def update_entity_position(self, old_position, new_position):
        entity = self.entity_positions.pop(old_position, None)
        if entity:
            self.entity_positions[new_position] = entity
            self.cells[new_position[0]][new_position[1]].set_element(entity)
            self.cells[old_position[0]][old_position[1]].set_element(Plant())
                
    def find_nearest_target(self, position, radius, target_type):
        i, j = position
        nearest_target = None
        min_distance = float('inf')
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                if self.is_target_in_range(i + di, j + dj, target_type):
                    distance = abs(di) + abs(dj)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_target = (i + di, j + dj)
        return nearest_target
    
    def is_target_in_range(self, i, j, target_type):
        return 0 <= i < self.size and 0 <= j < self.size and isinstance(self.cells[i][j].element, self.get_entity(target_type))
    
    def is_cell_overpopulated(self, i, j, max_neighbors=3):
        # Compter le nombre d'entités dans les cellules adjacentes
        count = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue 
                ni, nj = i + di, j + dj
                if 0 <= ni < self.size and 0 <= nj < self.size:
                    if not isinstance(self.cells[ni][nj].element, Plant):
                        count += 1
        return count > max_neighbors

    def get_random_valid_cell(self):
        count = 0
        while True:
            i, j = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if isinstance(self.cells[i][j].element, Plant) and not self.is_cell_overpopulated(i, j):
                return i, j
            elif count > 5 and  isinstance(self.cells[i][j].element, Plant):
                return i, j 
            count += 1
            
    def get_cell_info(self, i, j):
        return self.cells[i][j].element.get_info()
    
    def get_entity(self, target_type):
        if target_type == "Carrot": 
            return Carrot
        elif target_type == "Fox": 
            return Fox
        elif target_type == "Rabbit":
            return Rabbit
        return None

#------------------- methods Lokta-volterra -------------------#
    def count_predators_around(self, i, j):
        return sum(isinstance(cell.element, Fox) for cell in self.get_neighbours(i, j))
    
    def get_prey_around(self, i, j, prey_type):
        return [cell.element for cell in self.get_neighbours(i, j) if isinstance(cell.element, self.get_entity(prey_type))]
    
    def get_neighbours(self, i, j):
        neighbours = []
        for di, dj in MOVES:
            if 0 <= i + di < self.size and 0 <= j + dj < self.size:
                neighbours.append(self.cells[i + di][j + dj])
        return neighbours
    
    def distance_to_closest_prey(self, i, j, prey_type):
        pos_prey = self.find_nearest_target((i, j), 100, prey_type)
        if pos_prey:
            return abs(i - pos_prey[0]) + abs(j - pos_prey[1])
        return 1
# -------------------------------------------------------------#