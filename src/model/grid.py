import random
from src.constants import *
from model.cell import Cell
from model.flora import Carrot, Plant
from model.rabbit import Rabbit
from model.fox import Fox

class Grid:
    def __init__(self, size, speed, smart_level_rabbit, smart_level_fox):
        self.size = size
        self.speed = speed
        self.smart_level_rabbit = smart_level_rabbit
        self.smart_level_fox = smart_level_fox
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.turn = 0
        self.update_counter = 0
        self.entity_positions = {}
        self.count_rabbits = 0
        self.count_foxes = 0
        self.count_carrots = 0
        self.init_grid()


    def get_cell_info(self, i, j):
        return self.cells[i][j].element.get_info()
    
    def init_grid(self):
        num_rabbits = 1 # max(2, self.size // 10) 
        num_foxes = 1 #max(1, self.size // 20) 
        num_carrots = max(3, self.size // 5)

        self.add_entities(Rabbit, num_rabbits, smart_level=self.smart_level_rabbit)
        self.add_entities(Fox, num_foxes, smart_level=self.smart_level_fox)
        self.add_entities(Carrot, num_carrots)


    def add_entities(self, entity_class, num_entities, **kwargs):
        added = 0
        while added < num_entities:
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)
            if self.is_cell_valid(i, j):
                entity = entity_class(**kwargs)
                self.cells[i][j].set_element(entity)
                self.entity_positions[(i, j)] = entity
                added += 1
    
    def set_speed(self, speed):
        self.speed = speed
    
    def set_smart_level(self, smart_level_rabbit, smart_level_fox):
        self.smart_level_rabbit = smart_level_rabbit
        self.smart_level_fox = smart_level_fox
        for entity in self.entity_positions.values():
            if isinstance(entity, Rabbit):
                entity.set_smart_level(smart_level_rabbit)
            elif isinstance(entity, Fox):
                entity.set_smart_level(smart_level_fox)
    
  
    def update_systeme(self, force_update=False):
        if force_update or self.update_counter >= (SPEED_MAX  - self.speed):
            self.update_counter = 0  # Réinitialiser le compteur après la mise à jour
            self.turn += 1

            #self.adjust_population_controls()
            
            positions_to_update = list(self.entity_positions.keys())
            random.shuffle(positions_to_update) # Mélanger les positions pour éviter les biais de mise à jour
            for position in positions_to_update:
                i, j = position
                if position in self.entity_positions:
                    self.cells[i][j].update(i, j, self)
            
            if self.turn % TURN_SPAWN_CARROT == 0:  
                self.add_entities(Carrot, 1)
            
            self.update_count_population()
            print(f"tour {self.turn}")
        else:
            self.update_counter += 1  
        
    def remove_element(self, i, j):
        self.cells[i][j].set_element(Plant())
        self.entity_positions.pop((i, j), None)
    
    def is_cell_valid(self, i, j, entity_type=None):
        if not (0 <= i < self.size and 0 <= j < self.size):
            return False 

        cell_content = self.cells[i][j].element

        if entity_type is None:
            return isinstance(cell_content, Plant)
        elif entity_type == Rabbit:
            return isinstance(cell_content, Plant) or isinstance(cell_content, Carrot)
        elif entity_type == Fox:
            return isinstance(cell_content, Plant) or isinstance(cell_content, Rabbit)
        else:
            return False

    def update_entity_position(self, old_position, new_position):
        entity = self.entity_positions.pop(old_position, None)
        if entity:
            self.entity_positions[new_position] = entity
            self.cells[old_position[0]][old_position[1]].set_element(Plant())
            self.cells[new_position[0]][new_position[1]].set_element(entity)
    
    def find_nearest_target(self, position, radius, target_type):
        i, j = position
        nearest_target = None
        min_distance = float('inf')
        target = self.get_entity(target_type)
        
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                new_i, new_j = i + di, j + dj
                if 0 <= new_i < self.size and 0 <= new_j < self.size:
                    cell = self.cells[new_i][new_j]
                    if isinstance(cell.element, target):  
                        distance = abs(di) + abs(dj) 
                        if distance < min_distance:
                            min_distance = distance
                            nearest_target = (new_i, new_j)

        return nearest_target  
    
    def calculate_distance(self, position, target_position):
        i, j = position
        target_i, target_j = target_position
        return abs(i - target_i) + abs(j - target_j) 
    
    def get_entity(self, target_type):
        target = None
        if target_type == "Carrot":
            target = Carrot
        elif target_type == "Fox":
            target = Fox
        elif target_type == "Rabbit":
            target = Rabbit
        return target
    
    def count_population(self, entity_class):
        return sum(isinstance(entity, entity_class) for entity in self.entity_positions.values())

    def update_count_population(self):
        self.count_rabbits = self.count_population(Rabbit)
        self.count_foxes = self.count_population(Fox)
        self.count_carrots = self.count_population(Carrot)

    