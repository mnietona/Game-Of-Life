import random
from constants import *
from model.fauna import Fauna
from model.flora import Carrot

class Rabbit(Fauna):
    reproduction_rate = RABBIT_REPRODUCTION_RATE
    health_reproduction = RABBIT_HEALTH_REPRODUCTION

    def __init__(self, smart_level = 1):
        super().__init__(RABBIT_HEALTH, RABBIT_RADIUS) 
        self.target_type = Carrot
        self.base_radius = RABBIT_RADIUS
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()
        
    def adjust_radius_based_on_intelligence(self):
        self.radius = self.base_radius * self.smart_level
        
    def set_smart_level(self, smart_level):
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()   
        
    def update(self, i, j, grid):
        if self.smart_level > 2:
            from model.fox import Fox
            # voir si predateur à proximité
            predator_position = grid.find_nearest_target((i, j), self.radius, Fox)
            # voir si manger à proximité
            food_position = grid.find_nearest_target((i, j), self.radius, Carrot)
            # comparer la distance entre les deux
            if predator_position and food_position:
                ...
            # si distance vers manger < distance vers predateur, alors allez vers manger
            # sinon, fuite
            else:
                # Déplacer aléatoirement si rien n'est détecté
                self.move_randomly(i, j, grid)
                
        else:
            super().update(i, j, grid)
        
        
        if self.health_level >= self.health_reproduction and random.random() < self.reproduction_rate:
            self.reproduce(grid)
        
    def flee(self, i, j, grid, predator_position):
        ...
        
    def reproduce(self, grid):
        grid.add_entities(Rabbit, 1)
    
    @property
    def color(self):
        return WHITE