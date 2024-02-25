import random
from src.constants import *
from model.cell import Cell
from model.flora import Carrot, Plant, Burrow
from model.rabbit import Rabbit
from model.fox import Fox

class Grid:
    def __init__(self, size, speed, smart_level_rabbit, smart_level_fox, default_carrot_spawn, default_rabbits, default_foxes):
        self.size = size
        self.speed = speed
        self.smart_level_rabbit = smart_level_rabbit
        self.smart_level_fox = smart_level_fox
        self.carrot_spawn_speed = default_carrot_spawn 
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.entity_positions = {}
        self.burrow_positions = set()
        self.init_entities(default_rabbits, default_foxes)
        self.turn = 0
        self.update_counter = 0
        self.update_count_population()

    def init_entities(self, default_rabbits, default_foxes):
        self.init_burrows(2, 2) # Ajuster ici par rapport a la grille
        num_rabbits = default_rabbits if default_rabbits is not None else max(2, self.size // 10)
        num_foxes = default_foxes if default_foxes is not None else max(1, self.size // 20)
        self.populate_entities(Rabbit, num_rabbits, smart_level=self.smart_level_rabbit)
        self.populate_entities(Fox, num_foxes, smart_level=self.smart_level_fox)
        self.populate_entities(Carrot, max(3, self.size // 5))
    
    def init_burrows(self, num_burrows, burrow_size):
        for _ in range(num_burrows):
            while True:
                center_position = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
                if self.is_cell_valid_for_burrow(center_position, burrow_size):
                    break
            self.add_burrow(center_position, burrow_size)

    def populate_entities(self, entity_class, num_entities, smart_level=None, reproduce=False):
        for _ in range(num_entities):
            if reproduce and entity_class == Rabbit:
                i, j = self.get_random_burrow_position()
            else:
                i, j = self.get_random_valid_cell()

            self.add_entity(i, j, entity_class, smart_level)

    def get_random_valid_cell(self):
        while True:
            i, j = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if isinstance(self.cells[i][j].element, Plant):
                return i, j
    
    def get_random_burrow_position(self):
        available_burrows = [burrow_position for burrow_position in self.burrow_positions if isinstance(self.cells[burrow_position[0]][burrow_position[1]].element, Burrow)]
        if available_burrows:
            return random.choice(available_burrows)
        return self.get_random_valid_cell()

    def add_entity(self, i, j, entity_class, smart_level=None):
        kwargs = {}
        if entity_class != Carrot:
            kwargs['grid_size'] = self.size
        if smart_level is not None:
            kwargs['smart_level'] = smart_level
        entity = entity_class(**kwargs)
        self.cells[i][j].set_element(entity)
        self.entity_positions[(i, j)] = entity
    
    def add_burrow(self, center_position, burrow_size):
        i_center, j_center = center_position
        for i in range(i_center - burrow_size, i_center + burrow_size + 1):
            for j in range(j_center - burrow_size, j_center + burrow_size + 1):
                if 0 <= i < self.size and 0 <= j < self.size:
                    self.burrow_positions.add((i, j)) 
                    self.cells[i][j].set_element(Burrow())
                    self.entity_positions[(i, j)] = self.cells[i][j].element

    def is_cell_valid_for_burrow(self, center_position, burrow_size):
        i_center, j_center = center_position
        for i in range(i_center - burrow_size, i_center + burrow_size + 1):
            for j in range(j_center - burrow_size, j_center + burrow_size + 1):
                if not (0 <= i < self.size and 0 <= j < self.size): # Pas dans la grille
                    return False 
        return True
    
    def update_system(self, force_update=False):
        if self.should_update(force_update):
            self.update_entities()
            self.spawn_carrots()
            self.print_turn_info()
            self.update_count_population()
            self.turn += 1
            self.update_counter = 0
        else:
            self.update_counter += 1    

    def should_update(self, force_update):
        return self.update_counter >= (SPEED_MAX - self.speed) or self.turn == 0 or force_update

    def update_entities(self):
        positions_to_update = list(self.entity_positions.keys())
        random.shuffle(positions_to_update) 
        for position in positions_to_update:
            i, j = position
            if position in self.entity_positions:
                self.cells[i][j].update(i, j, self)

    def spawn_carrots(self):
        if self.turn % (TURN_SPAWN_CARROT - self.carrot_spawn_speed) == 0:
            self.populate_entities(Carrot, 1)

    def print_turn_info(self):
        print(f"Turn: {self.turn}")
    
    def update_count_population(self):
        self.count_rabbits = sum(isinstance(entity, Rabbit) for entity in self.entity_positions.values())
        self.count_foxes = sum(isinstance(entity, Fox) for entity in self.entity_positions.values())
        self.count_carrots = sum(isinstance(entity, Carrot) for entity in self.entity_positions.values())
    
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
    
    def set_speed(self, speed):
        self.speed = speed
    
    def set_carrot_spawn_speed(self, carrot_spawn_speed):
        self.carrot_spawn_speed = carrot_spawn_speed

    def set_smart_level(self, smart_level_rabbit, smart_level_fox):
        self.smart_level_rabbit, self.smart_level_fox = smart_level_rabbit, smart_level_fox
        self.apply_smart_levels()

    def apply_smart_levels(self):
        for _, entity in self.entity_positions.items():
            if isinstance(entity, Rabbit):
                entity.set_smart_level(self.smart_level_rabbit)
            elif isinstance(entity, Fox):
                entity.set_smart_level(self.smart_level_fox)
    
    def remove_element(self, i, j):
        if (i, j) in self.entity_positions:
            del self.entity_positions[(i, j)]
            if (i, j) in self.burrow_positions:
                self.cells[i][j].set_element(Burrow())
            else:
                self.cells[i][j].set_element(Plant())
            
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

    def update_entity_position(self, old_position, new_position):
        entity = self.entity_positions.pop(old_position, None)
        if entity:
            is_leaving_burrow = old_position in self.burrow_positions
            
            self.entity_positions[new_position] = entity
            self.cells[new_position[0]][new_position[1]].set_element(entity)
            
            if is_leaving_burrow:
                self.cells[old_position[0]][old_position[1]].set_element(Burrow()) 
            else:
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
    
    def calculate_distance(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

    def find_nearest_burrow(self, position):
        nearest_burrow = None
        min_distance = float('inf')
        for burrow_position in self.burrow_positions:
            distance = self.calculate_distance(position, burrow_position)
            if distance < min_distance:
                min_distance = distance
                nearest_burrow = burrow_position
        return nearest_burrow