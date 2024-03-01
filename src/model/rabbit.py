from constants import *
from model.fauna import Fauna

# Constantes de lapin
ALPHA = 0.08  # Taux de reproduction des lapins
BETA = 0.05   # Taux de mortalité des lapins dû aux renards

class Rabbit(Fauna):
    def __init__(self, grid_size, smart_level=1):
        super().__init__(grid_size, health=RABBIT_HEALTH, radius=RABBIT_RADIUS, delta=RABBIT_DELTA_RADIUS)
        self.prey = "Carrot"
        self.smart_level = smart_level

    def interact_with_environment(self, i, j, grid):
        # Mortalité naturelle due aux prédateurs et à la vieillesse
        if grid.count_predators_around(i, j) > 0:
            self.health = 0
            if grid.count_population(Rabbit) <= 3:
                grid.populate_entities(Rabbit, 2)
            return
        
        carrots_eaten = self.eat_carrots(i, j, grid)
        # Une reproduction a lieux tout les 7 tours
        if carrots_eaten > 0:
            self.health += ALPHA * carrots_eaten
            if self.health > RABBIT_SOME_REPRODUCTION_THRESHOLD:
                self.health -= RABBIT_COST_OF_REPRODUCTION
                if grid.count_population(Rabbit) < (grid.size**2)/4:
                    grid.populate_entities(Rabbit, 3)
                
    def eat_carrots(self, i, j, grid):
        l_carrots = grid.get_prey_around(i, j, "Carrot")
        for carrot in l_carrots:
            carrot.health = 0
        return len(l_carrots)

    @property
    def color(self):
        return WHITE
