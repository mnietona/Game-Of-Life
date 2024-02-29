from constants import *
from model.fauna import Fauna

GAMMA = 0.4  # Taux de mortalité des renards
DELTA = 0.075  # Taux de reproduction des renards en fonction des lapins mangés
HUNGER_THRESHOLD = 5  # Seuil de faim pour qu'un renard mange un lapin
FOX_HEALTH = 100  # Santé initiale des renards
FOX_REPRODUCTION_RATE = 90  # Santé nécessaire pour qu'un renard se reproduise
FOX_RADIUS = 2  # Rayon de déplacement des renards
DELTA_RADIUS = 0  # Rayon de déplacement des renards

class Fox(Fauna):
    def __init__(self, grid_size):
        super().__init__(grid_size, health=FOX_HEALTH, reproduction_rate=FOX_REPRODUCTION_RATE, radius=FOX_RADIUS, delta=DELTA_RADIUS)
        self.hunger = 0 
        self.prey = "Rabbit"

    def interact_with_environment(self, i, j, env):
        self.health -= GAMMA
        
        rabbits_eaten = self.eat_rabbits(i, j, env.grid)
        if rabbits_eaten > 0:
            self.health += DELTA * rabbits_eaten
        
        # Vérifiez si la santé permet la reproduction
        if self.health > self.reproduction_rate:
            self.health -= 100  # Diminution de la santé après la reproduction
            env.populate_entities(Fox, 1)


    def eat_rabbits(self, i, j, grid):
        # Manger des lapins si possible
        rabbits_eaten = 0
        for rabbit in grid.get_prey_around(i, j, self.prey):
            #if self.hunger >= HUNGER_THRESHOLD: # Il mange si rencontre 5 fois 1 lapin 
            rabbit.health = 0  # 
            rabbits_eaten += 1
            self.health += 10
            self.hunger = 0
            self.hunger += 1
        return rabbits_eaten


    
    @property
    def color(self):
        return RED
    