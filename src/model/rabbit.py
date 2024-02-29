from constants import *
from model.fauna import Fauna

# Constantes de lapin
ALPHA = 0.35  # Taux de reproduction des lapins
BETA = 0.02   # Taux de mortalité des lapins dû aux renards
RABBIT_HEALTH = 50
RABBIT_SOME_REPRODUCTION_THRESHOLD = 30
RABBIT_COST_OF_REPRODUCTION = 10

class Rabbit(Fauna):
    def __init__(self, grid_size):
        super().__init__(grid_size, health=RABBIT_HEALTH, radius=RABBIT_RADIUS, delta=RABBIT_DELTA_RADIUS)
        self.prey = "Carrot"

    def interact_with_environment(self, i, j, env):
        # Mortalité naturelle due aux prédateurs et à la vieillesse
        self.health -= BETA * env.grid.count_predators_around(i, j)
        
        carrots_eaten = self.eat_carrots(i, j, env.grid)
        
        if carrots_eaten > 0:
            self.health += ALPHA * carrots_eaten
            if self.health > RABBIT_SOME_REPRODUCTION_THRESHOLD:
                self.health -= RABBIT_COST_OF_REPRODUCTION
                env.populate_entities(Rabbit, 1)
                
    def eat_carrots(self, i, j, grid):
        l_carrots = grid.get_prey_around(i, j, "Carrot")
        for carrot in l_carrots:
            carrot.health = 0
        return len(l_carrots)

    @property
    def color(self):
        return WHITE
