import random
from src.constants import *
from model.grid import Grid
from model.flora import Carrot, Burrow
from model.rabbit import Rabbit
from model.fox import Fox

class Simulation:
    def __init__(self, size, speed, smart_level_rabbit, smart_level_fox, default_carrot_spawn, default_rabbits, default_foxes):
        self.grid = Grid(size)
        self.speed = speed
        self.smart_level_rabbit = smart_level_rabbit
        self.smart_level_fox = smart_level_fox
        self.carrot_spawn_speed = default_carrot_spawn
        self.turn = 0
        self.update_counter = 0
        self.init_entities(default_rabbits, default_foxes)
        self.update_count_population()
    
    def init_entities(self, default_rabbits, default_foxes):
        num_burrows = max(1, self.grid.size // 20)
        burrow_size = max(1, self.grid.size // 40)
        self.grid.initialize_burrows(num_burrows, burrow_size)
        
        num_rabbits = default_rabbits if default_rabbits is not None else max(2, self.grid.size // 3)
        num_foxes = default_foxes if default_foxes is not None else num_rabbits // 2
        self.grid.populate_entities(Rabbit, num_rabbits, smart_level=self.smart_level_rabbit)
        self.grid.populate_entities(Fox, num_foxes, smart_level=self.smart_level_fox)
        self.grid.populate_entities(Carrot, max(3, self.grid.size // 5))
    
    def update_system(self, force_update=False):
        if self.should_update(force_update):
            self.update_entities()
            self.spawn_carrots()
            self.update_count_population()
            self.ajust_population()
            self.turn += 1
            self.update_counter = 0
        else:
            self.update_counter += 1 
    
    def should_update(self, force_update):
        return self.update_counter >= (SPEED_MAX - self.speed) or self.turn == 0 or force_update

    def update_entities(self):
        positions_to_update = list(self.grid.entity_positions.keys())
        random.shuffle(positions_to_update) 
        for position in positions_to_update:
            i, j = position
            if position in self.grid.entity_positions:
                self.grid.cells[i][j].update(i, j, self)

    def spawn_carrots(self):
        if self.turn % (TURN_SPAWN_CARROT - self.carrot_spawn_speed) == 0:
            self.grid.populate_entities(Carrot, 1)

    def update_count_population(self):
        self.count_rabbits = self.grid.count_population(Rabbit)
        self.count_foxes = self.grid.count_population(Fox)
        self.count_carrots = self.grid.count_population(Carrot)
    
    def ajust_population(self):
        # Ajuste la population qui disparait
        if self.count_rabbits == 0:
            self.grid.populate_entities(Rabbit, 3)
        if self.count_foxes == 0:
            self.grid.populate_entities(Fox, 3)
    
    def set_speed(self, speed):
        self.speed = speed
    
    def set_carrot_spawn_speed(self, carrot_spawn_speed):
        self.carrot_spawn_speed = carrot_spawn_speed

    def set_smart_level(self, smart_level_rabbit, smart_level_fox):
        self.smart_level_rabbit, self.smart_level_fox = smart_level_rabbit, smart_level_fox
        self.apply_smart_levels()

    def apply_smart_levels(self):
        for _, entity in self.grid.entity_positions.items():
            if isinstance(entity, Rabbit):
                entity.set_smart_level(self.smart_level_rabbit)
            elif isinstance(entity, Fox):
                entity.set_smart_level(self.smart_level_fox)
