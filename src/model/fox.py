from constants import *
from model.fauna import Fauna

FOX_REPRODUCTION_RATE = 0.02 # 5% de chance de se reproduire
FOX_HEALTH_REPRODUCTION = 200

class Fox(Fauna):
    
    def __init__(self, grid_size, smart_level = 1):
        super().__init__(FOX_HEALTH, FOX_RADIUS, FOX_HEALTH_REPRODUCTION, FOX_REPRODUCTION_RATE, grid_size, delta=-1)
        self.target_type = "Rabbit"
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()  
        self.hunger_level = 0  # Niveau de faim initial
        self.hunger_threshold = 5  
    
    def update(self, i, j, env):
        grid = env.grid
        self.hunger_level += 1
        super().update(i, j, env)
        if self.age % 10 == 0:
            self.try_reproduce(grid)
    
    def eat_if_possible(self, position, grid):
        if self.hunger_level >= self.hunger_threshold:
            entity_at_new_position = grid.entity_positions.get(position)
            if entity_at_new_position and isinstance(entity_at_new_position, grid.get_entity(self.target_type)):
                self.health += entity_at_new_position.health
                self.hunger_level = 0

    @property
    def color(self):
        return RED