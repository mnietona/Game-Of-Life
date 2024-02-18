from constants import *

class Flora:
    def __init__(self, health_level):
        self.health_level = health_level

    def get_info(self):
        if self.health_level == float('inf'):
            return f"{self.__class__.__name__}- Durée de vie: éternelle"
        
        return f"{self.__class__.__name__}- Durée de vie: {self.health_level}"

    def update(self, i, j, grid): 
        self.health_level -= 1 if self.health_level > 0 else grid.remove_element(i, j)
     
    @property
    def color(self):
        return BLACK

class Plant(Flora):
    def __init__(self, health_level=float('inf')):
        super().__init__(health_level)
    
    @property
    def color(self):
        return GREEN

class Carrot(Flora):
    def __init__(self, health_level=CARROT_HEALTH):
        super().__init__(health_level)
    
    @property
    def color(self):
        return ORANGE
