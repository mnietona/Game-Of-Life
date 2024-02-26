from constants import *
from model.fauna import Fauna

class Rabbit(Fauna):

    def __init__(self, grid_size, smart_level = 1):
        super().__init__(RABBIT_HEALTH, RABBIT_RADIUS, RABBIT_HEALTH_REPRODUCTION, RABBIT_REPRODUCTION_RATE, grid_size, delta=2)
        self.target_type = "Carrot"
        self.predator_type = "Fox"
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()
    
    @property
    def color(self):
        return WHITE
        
    def update(self, i, j, grid):
        if self.smart_level > 1:
            self.decrease_health()
            if self.is_alive():
                self.intelligent_behavior(i, j, grid)
            else:
                grid.remove_element(i, j)
        else:
            super().update(i, j, grid)
            
        if self.age % 5 == 0:
            self.try_reproduce(grid)
    
    def intelligent_behavior(self, i, j, grid):
        position = (i, j)
        food_position = grid.find_nearest_target(position, self.radius, self.target_type)
        predator_position = grid.find_nearest_target(position, self.radius, self.predator_type)

        new_position = self.decide_action(position, food_position, predator_position, grid)
        
        if new_position != position:
            self.eat_if_possible(new_position, grid)
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

        if predator_distance < food_distance:
            return self.flee(position, predator_position, grid)
        else:
            return self.move_towards(position, food_position, grid)
    
    def flee(self, current_position, predator_position, grid):
        possible_moves = self.get_possible_moves(current_position, grid)
        best_move = None
        best_score = float('-inf')
        
        burrow_position = None
        if self.smart_level == 3:
            burrow_position = grid.find_nearest_burrow(current_position)

        for move in possible_moves:
            distance_to_predator = self.calculate_distance(move, predator_position)
            
            distance_to_burrow = self.calculate_distance(move, burrow_position) if self.smart_level == 3 and burrow_position else float('inf')
            
            score = distance_to_predator - distance_to_burrow if self.smart_level == 3 else distance_to_predator
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move if best_move else self.move_towards(current_position, predator_position, grid, flee=True)



