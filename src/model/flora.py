from constants import *

class Flora:
    def __init__(self, health):
        self.health = health

    def get_info(self):
        if self.health == float('inf'):
            return f"{self.__class__.__name__}- Durée de vie: éternelle"
        
        return f"{self.__class__.__name__}- Durée de vie: {self.health}"

    def update(self, i, j, env): 
        if self.health > 0 :
            self.health -= 1 
        else:
            env.grid.remove_element(i, j)
     
    @property
    def color(self):
        return BLACK

class Plant(Flora):
    def __init__(self, health=float('inf')):
        super().__init__(health)
    
    @property
    def color(self):
        return GREEN

class Carrot(Flora):
    def __init__(self, health=CARROT_HEALTH):
        super().__init__(health)
    
    @property
    def color(self):
        return ORANGE
    
class Burrow(Flora):
    def __init__(self, num, health=float('inf')):
        super().__init__(health)
        self.num = num

    @property
    def color(self):
        return LIGHT_GREY