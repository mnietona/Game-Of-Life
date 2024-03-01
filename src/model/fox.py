from constants import *
import random
from model.fauna import Fauna

# Constantes de renard
GAMMA = 0.001 # Taux de mortalité des renards dû à la vieillesse
DELTA =  5  # Taux de gain de santé des renards dû à la chasse


class Fox(Fauna):
    def __init__(self, grid_size):
        super().__init__(grid_size, health=FOX_HEALTH, radius=FOX_RADIUS, delta=FOX_DELTA_RADIUS)
        self.prey = "Rabbit"

    def interact_with_environment(self, i, j, env):
        # Mortalité naturelle due à la vieillesse
        self.health -= GAMMA * self.age
    
        # Manger des lapins pour gagner de la santé
        rabbits_eaten = self.eat_rabbits(i, j, env.grid)
        if rabbits_eaten > 0 or env.grid.count_population(Fox) < 2:
            if env.grid.count_population(Fox) <= 2:
                self.health += FOX_HEALTH
                num_fox = 5
            else:
                self.health += DELTA * rabbits_eaten
                num_fox = 1
            # Se reproduire si la santé est suffisante après avoir mangé
            if self.health > FOX_SOME_REPRODUCTION_THRESHOLD:
                self.health -= FOX_COST_OF_REPRODUCTION
                if env.grid.count_population(Fox) < (env.grid.size**2)/4:
                    env.populate_entities(Fox, num_fox)
        else:
            self.health -= DELTA
        
            
    def eat_rabbits(self, i, j, grid):
        l_rabbits = grid.get_prey_around(i, j, "Rabbit")
        for rabbit in l_rabbits:
            rabbit.health = 0
        return len(l_rabbits)

    @property
    def color(self):
        return RED
