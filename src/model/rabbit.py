import random
from constants import *
from model.fauna import Fauna

class Rabbit(Fauna):

    def __init__(self, smart_level = 1):
        super().__init__(RABBIT_HEALTH, RABBIT_RADIUS, RABBIT_HEALTH_REPRODUCTION, RABBIT_REPRODUCTION_RATE)
        self.target_type = "Carrot"
        self.predator_type = "Fox"
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()
        
    def adjust_radius_based_on_intelligence(self):
        self.radius = RABBIT_RADIUS * self.smart_level
        
    def set_smart_level(self, smart_level):
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()   
        
    def update(self, i, j, grid):
        if self.smart_level > 1:
            self.intelligent_behavior(i, j, grid)
        else:
            super().update(i, j, grid)

        self.try_reproduce(grid)
    
    def intelligent_behavior(self, i, j, grid):
        position = (i, j)
        food_position = grid.find_nearest_target(position, self.radius, self.target_type)
        predator_position = grid.find_nearest_target(position, self.radius, self.predator_type)

        new_position = self.decide_action(position, food_position, predator_position, grid)
        grid.update_entity_position(position, new_position)

    def decide_action(self, position, food_position, predator_position, grid):
        if predator_position and food_position:
            return self.evaluate_threat_and_food(position, food_position, predator_position, grid)
        elif predator_position:
            return self.flee(position, predator_position, grid)
        elif food_position:
            return self.move_towards(position, food_position, grid)
        else:
            return self.move_randomly(position[0], position[1], grid)

    def evaluate_threat_and_food(self, position, food_position, predator_position, grid):
        predator_distance = self.calculate_distance(position, predator_position)
        food_distance = self.calculate_distance(position, food_position)

        if food_distance < predator_distance:
            return self.move_towards(position, food_position, grid)
        else:
            return self.flee(position, predator_position, grid)

        
    def flee(self,current_position, predator_position, grid):
        return self.move_towards(current_position, predator_position, grid, flee=True)
        
    @property
    def color(self):
        return WHITE