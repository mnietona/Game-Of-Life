import random
from src.constants import *
from model.fauna import Fauna
from model.rabbit import Rabbit


class Fox(Fauna):
    reproduction_rate = FOX_REPRODUCTION_RATE
    health_reproduction = FOX_HEALTH_REPRODUCTION
    
    def __init__(self, health_level=FOX_HEALTH, radius=FOX_RADIUS):
        super().__init__(health_level, radius)
        self.target_type = Rabbit
        
    
    def update(self, i, j, grid):
        super().update(i, j, grid)
        
        if self.health_level >= self.health_reproduction and random.random() < self.reproduction_rate:
            self.reproduce(grid)
        
    def reproduce(self, grid):
        grid.add_entities(Fox, 1)

    @property
    def color(self):
        return RED