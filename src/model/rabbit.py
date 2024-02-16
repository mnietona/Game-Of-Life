import random
from src.constants import *
from model.fauna import Fauna
from model.flora import Carrot

class Rabbit(Fauna):
    def __init__(self, health_level=RABBIT_HEALTH, radius=RABBIT_RADIUS):
        super().__init__(health_level, radius) 
        self.target_type = Carrot
    
    def update(self, i, j, grid):
        super().update(i, j, grid)
        
        if self.health_level >= RABBIT_HEALTH_REPRODUCTION and random.random() < RABBIT_REPRODUCTION_RATE:
            self.reproduce(grid)
        
    def reproduce(self, grid):
        grid.add_entities(Rabbit, 1)
    
    @property
    def color(self):
        return WHITE