from constants import *
from model.fauna import Fauna

class Fox(Fauna):
    
    def __init__(self, smart_level = 1):
        super().__init__(FOX_HEALTH, FOX_RADIUS, FOX_HEALTH_REPRODUCTION, FOX_REPRODUCTION_RATE)
        self.target_type = "Rabbit"
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()
    
    def adjust_radius_based_on_intelligence(self):
        self.radius = FOX_RADIUS * self.smart_level
    
    def set_smart_level(self, smart_level):
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()      
    
    def update(self, i, j, grid):
        super().update(i, j, grid)
        self.try_reproduce(grid)

    @property
    def color(self):
        return RED