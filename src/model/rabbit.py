from constants import *
from model.fauna import Fauna
import random

ALPHA = 1.1  # Taux de reproduction des lapins
BETA = 0.4   # Taux de mortalité des lapins dû aux renards
RABBIT_HEALTH = 50 # Santé initiale des lapins
RABBIT_REPRODUCTION_RATE = 20  # Santé nécessaire pour qu'un lapin se reproduise
RABBIT_RADIUS = 5  # Rayon de déplacement des lapins
DELTA_RADIUS = 2  # Rayon de déplacement des lapins

class Rabbit(Fauna):
    def __init__(self, grid_size):
        super().__init__(grid_size, health=RABBIT_HEALTH, reproduction_rate=RABBIT_REPRODUCTION_RATE, radius=RABBIT_RADIUS, delta=DELTA_RADIUS)
        self.prey = "Carrot"

    def interact_with_environment(self, i, j, env):
        self.health -= BETA * env.grid.count_predators_around(i, j)
        
        carrots_eaten = self.eat_carrots(i, j, env.grid)
        if carrots_eaten > 0:
            self.health += ALPHA * carrots_eaten
            # Vérifiez si la santé permet la reproduction
            if self.health > self.reproduction_rate:
                self.health -= self.reproduction_rate  # Assurez-vous de diminuer la santé après la reproduction
                env.populate_entities(Rabbit, 1)
            

    
    def eat_carrots(self, i, j, grid):
        # Manger des carottes si possible
        carrots_eaten = 0
        for carrot in grid.get_prey_around(i, j, self.prey):
            carrot.health = 0
            carrots_eaten += 1
            self.health += 10
        return carrots_eaten
        
    
    @property
    def color(self):
        return WHITE
        
