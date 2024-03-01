import random
from constants import *
from model.cell import Cell
from model.flora import Carrot, Plant, Burrow
from model.rabbit import Rabbit
from model.fox import Fox

class Grid:
    def __init__(self, size):
        self.size = size
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.entity_positions = {}
        self.burrow_positions = set()
    
    def initialize_burrows(self, num_burrows, burrow_size):
        for num in range(num_burrows):
            while True:
                center_position = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
                if self.is_cell_valid_for_burrow(center_position, burrow_size):
                    break
            self.add_burrow(center_position, burrow_size, num+1)
    
    def populate_entities(self, entity_class, count, smart_level=None, reproduce=False):
        for _ in range(count):
            position = self.get_random_position_for_entity(entity_class, reproduce)
            self.add_entity(entity_class, position, smart_level)

    def get_random_position_for_entity(self, entity_class, reproduce):
        if reproduce and entity_class == Rabbit:
            return self.get_random_burrow_position()
        return self.get_random_valid_cell()

    def add_entity(self, entity_class, position, smart_level=None):
        i, j = position
        kwargs = {'grid_size': self.size} if entity_class != Carrot else {}
        if smart_level is not None:
            kwargs['smart_level'] = smart_level
        entity = entity_class(**kwargs)
        self.cells[i][j].set_element(entity)
        self.entity_positions[(i, j)] = entity

    def add_burrow(self, center_position, burrow_size, num_burrow):
        i_center, j_center = center_position
        for i in range(i_center - burrow_size, i_center + burrow_size + 1):
            for j in range(j_center - burrow_size, j_center + burrow_size + 1):
                if 0 <= i < self.size and 0 <= j < self.size:
                    self.burrow_positions.add((i, j)) 
                    self.cells[i][j].set_element(Burrow(num_burrow))
                    self.entity_positions[(i, j)] = self.cells[i][j].element
    
    def remove_element(self, i, j):
        if (i, j) in self.entity_positions:
            del self.entity_positions[(i, j)]
            if (i, j) in self.burrow_positions:
                self.cells[i][j].set_element(Burrow(0))
            else:
                self.cells[i][j].set_element(Plant())
             
    def update_entity_position(self, old_position, new_position):
        entity = self.entity_positions.pop(old_position, None)
        if entity:
            is_leaving_burrow = old_position in self.burrow_positions
            
            self.entity_positions[new_position] = entity
            self.cells[new_position[0]][new_position[1]].set_element(entity)
            
            if is_leaving_burrow:
                self.cells[old_position[0]][old_position[1]].set_element(Burrow(0)) 
            else:
                self.cells[old_position[0]][old_position[1]].set_element(Plant())
    
    def count_population(self, entity_type):
        return sum(isinstance(entity, entity_type) for entity in self.entity_positions.values())
    
    def calculate_distance(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1]) # Manhattan distance
        
    def find_nearest_target(self, position, radius, target_type):
        i, j = position
        nearest_target = None
        min_distance = float('inf')
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                if self.is_target_in_range(i + di, j + dj, target_type):
                    distance = self.calculate_distance((i, j), (i + di, j + dj))
                    if distance < min_distance:
                        min_distance = distance
                        nearest_target = (i + di, j + dj)
        return nearest_target

    def find_nearest_burrow(self, position):
        nearest_burrow = None
        min_distance = float('inf')
        for burrow_position in self.burrow_positions:
            distance = self.calculate_distance(position, burrow_position)
            if distance < min_distance:
                min_distance = distance
                nearest_burrow = burrow_position
        return nearest_burrow

    def is_cell_valid(self, i, j, entity_type=None):
        if not (0 <= i < self.size and 0 <= j < self.size):
            return False 
        cell_content = self.cells[i][j].element
        if entity_type is None:
            return isinstance(cell_content, Plant)
        elif entity_type == Rabbit:
            return isinstance(cell_content, (Plant, Carrot, Burrow)) 
        elif entity_type == Fox:
            return isinstance(cell_content, (Plant, Rabbit)) and (i, j) not in self.burrow_positions
        else:
            return False
       
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

    def is_cell_valid_for_burrow(self, center_position, burrow_size):
        i_center, j_center = center_position

        for i in range(i_center - burrow_size, i_center + burrow_size + 1):
            for j in range(j_center - burrow_size, j_center + burrow_size + 1):
                if not (0 <= i < self.size and 0 <= j < self.size): 
                    return False
        
        for existing_center in self.burrow_positions:
            if self.calculate_distance(center_position, existing_center) < 20: # 20 pcq ca foncitonne le mieux
                return False
        return True
    
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

    def get_random_burrow_position(self):
        available_burrows = [burrow_position for burrow_position in self.burrow_positions if isinstance(self.cells[burrow_position[0]][burrow_position[1]].element, Burrow)]
        if available_burrows:
            return random.choice(available_burrows)
        return self.get_random_valid_cell()

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
            return self.calculate_distance((i, j), pos_prey)
        return 1
# -------------------------------------------------------------#