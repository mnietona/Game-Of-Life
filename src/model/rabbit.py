import random
from constants import *
from model.fauna import Fauna

class Rabbit(Fauna):
    reproduction_rate = RABBIT_REPRODUCTION_RATE
    health_reproduction = 100000000000 #RABBIT_HEALTH_REPRODUCTION

    def __init__(self, smart_level = 1):
        super().__init__(RABBIT_HEALTH, RABBIT_RADIUS) 
        self.target_type = "Carrot"
        self.predator_type = "Fox"
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
            position = (i, j)
            new_position = position
            food_position = grid.find_nearest_target(position, self.radius, self.target_type)
            predator_position = grid.find_nearest_target(position, self.radius, self.predator_type)
            
            if food_position and predator_position:
                predator_distance = grid.calculate_distance(position, predator_position)
                food_distance = grid.calculate_distance(position, food_position)
                
                if predator_distance < food_distance:
                    new_position = self.flee(position, predator_position, grid)
                else:
                    new_position = self.move_towards(position, food_position, grid)
            elif predator_position:
                new_position = self.flee(position, predator_position, grid)
            elif food_position:
                new_position = self.move_towards(position, food_position, grid)
            else:
                new_position = self.move_randomly(i, j, grid)
            grid.update_entity_position(position, new_position)
        else:
            super().update(i, j, grid)

        if self.health_level >= self.health_reproduction and random.random() < self.reproduction_rate:
            self.reproduce(grid)

        
    def flee(self,current_position, predator_position, grid):
        return self.move_towards(current_position, predator_position, grid, flee=True)
        
        
        
    def reproduce(self, grid):
        grid.add_entities(Rabbit, 1)
    
    @property
    def color(self):
        return WHITE