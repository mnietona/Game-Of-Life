from constants import *
from model.fauna import Fauna

# Constantes de renard
GAMMA = 0.01 # Taux de mortalité des renards dû à la vieillesse
DELTA = 0.47 # Taux de gain de santé des renards dû à la chasse
FOX_HEALTH = 70
FOX_SOME_REPRODUCTION_THRESHOLD = 50
FOX_COST_OF_REPRODUCTION = 20

class Fox(Fauna):
    def __init__(self, grid_size):
        super().__init__(grid_size, health=FOX_HEALTH, radius=FOX_RADIUS, delta=FOX_DELTA_RADIUS)
        self.prey = "Rabbit"

    def interact_with_environment(self, i, j, env):
        # Mortalité naturelle due à la vieillesse
        self.health -= GAMMA * self.age
        
        # Manger des lapins pour gagner de la santé
        rabbits_eaten = self.eat_rabbits(i, j, env.grid)
        if rabbits_eaten > 0:
            self.health += DELTA * rabbits_eaten
            # Se reproduire si la santé est suffisante après avoir mangé
            if self.health > FOX_SOME_REPRODUCTION_THRESHOLD:
                self.health -= FOX_COST_OF_REPRODUCTION
                env.populate_entities(Fox, 1)
        
        else:
            # Mortalité naturelle due à la faim
            self.health -= DELTA
    
    def eat_rabbits(self, i, j, grid):
        l_rabbits = grid.get_prey_around(i, j, "Rabbit")
        for rabbit in l_rabbits:
            rabbit.health = 0
        return len(l_rabbits)

    @property
    def color(self):
        return RED
