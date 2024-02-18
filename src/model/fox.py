import random
from constants import *
from model.fauna import Fauna
from model.rabbit import Rabbit


class Fox(Fauna):
    reproduction_rate = FOX_REPRODUCTION_RATE
    health_reproduction = FOX_HEALTH_REPRODUCTION
    
    def __init__(self, smart_level = 1):
        super().__init__(FOX_HEALTH, FOX_RADIUS)
        self.target_type = Rabbit
        self.base_radius = FOX_RADIUS
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()
    
    def adjust_radius_based_on_intelligence(self):
        self.radius = self.base_radius * self.smart_level
    
    def set_smart_level(self, smart_level):
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()      
    
    def update(self, i, j, grid):
        super().update(i, j, grid)
        
        if self.health_level >= self.health_reproduction and random.random() < self.reproduction_rate:
            self.reproduce(grid)
        
    def reproduce(self, grid):
        grid.add_entities(Fox, 1)

    @property
    def color(self):
        return RED