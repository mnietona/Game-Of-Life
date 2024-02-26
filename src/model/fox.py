from constants import *
from model.fauna import Fauna

class Fox(Fauna):
    
    def __init__(self, grid_size, smart_level = 1):
        super().__init__(FOX_HEALTH, FOX_RADIUS, FOX_HEALTH_REPRODUCTION, FOX_REPRODUCTION_RATE, grid_size, delta=-1)
        self.target_type = "Rabbit"
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()  
    
    def update(self, i, j, grid):
        super().update(i, j, grid)
        if self.age % 10 == 0:
            self.try_reproduce(grid)

    @property
    def color(self):
        return RED