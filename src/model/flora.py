from constants import *

class Flora:
    def __init__(self, health):
        self.health = health

    def get_info(self):
        if self.health == float('inf'):
            return f"{self.name_fr()}- Durée de vie: éternelle"
        
        return f"{self.name_fr()}- Durée de vie: {self.health}"

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
    
    def name_fr(self):
        return "Plante"
    
    @property
    def color(self):
        return GREEN

class Carrot(Flora):
    def __init__(self, health=CARROT_HEALTH):
        super().__init__(health)
    
    def name_fr(self):
        return "Carotte"
    
    @property
    def color(self):
        return ORANGE
    
class Burrow(Flora):
    def __init__(self, num, health=float('inf')):
        super().__init__(health)
        self.num = num
    
    def name_fr(self):
        return f"Terrier"

    @property
    def color(self):
        return LIGHT_GREY