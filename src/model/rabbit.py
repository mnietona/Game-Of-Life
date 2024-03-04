from constants import *
from model.fauna import Fauna

class Rabbit(Fauna):

    def __init__(self, grid_size, smart_level = 1):
        super().__init__(grid_size, health=RABBIT_HEALTH, radius=RABBIT_RADIUS, delta=RABBIT_DELTA_RADIUS)
        self.target_type = "Carrot"
        self.predator_type = "Fox"
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()

    def interact_with_environment(self, i, j, grid):
        self.precalculate_distances((i, j), grid)
        new_position = self.intelligent_behavior(i, j, grid)
        self.after_interaction(new_position, grid)
        return new_position

    def precalculate_distances(self, position ,grid):
        self.distance_to_nearest_predator = grid.find_nearest_target(position, self.radius, self.predator_type)
        self.distance_to_nearest_food = grid.find_nearest_target(position, self.radius, self.target_type)
        self.distance_to_nearest_burrow = grid.find_nearest_burrow(position)
        self.predator_distance = grid.calculate_distance(position, self.distance_to_nearest_predator)
        self.food_distance = grid.calculate_distance(position, self.distance_to_nearest_food)

    def intelligent_behavior(self, i, j, grid):
        position = (i, j)
        if self.smart_level > 1: 
            new_position = self.decide_action(position, self.distance_to_nearest_food , self.distance_to_nearest_predator, grid)
        else:
            new_position = self.move(i, j, grid)
            
        return new_position

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

        if self.predator_distance < self.food_distance:
            return self.flee(position, predator_position, grid)
        else:
            return self.move_towards(position, food_position, grid)
    
    def flee(self, position, predator_position, grid):
        valid_moves = self.get_valid_moves(position, grid)
        if not valid_moves: 
            return position
        if self.smart_level == 2:
            return max(valid_moves, key=lambda move: grid.calculate_distance(move, predator_position))
        elif self.smart_level == 3:
            return self.best_move_to_flee(valid_moves, predator_position, position, grid)
    
    def best_move_to_flee(self, valid_moves, predator_position, current_position, grid):
        best_move = current_position
        best_score = float('-inf')

        for move in valid_moves:
            distance_to_predator_after_move = grid.calculate_distance(move, predator_position)
            distance_to_burrow_after_move = grid.calculate_distance(move, self.distance_to_nearest_burrow)
            
            score = distance_to_predator_after_move - distance_to_burrow_after_move

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def try_reproduce(self, grid):
        if self.health > RABBIT_SOME_REPRODUCTION_THRESHOLD:
            self.health -= RABBIT_COST_OF_REPRODUCTION
            if grid.count_population(Rabbit) < (grid.size**2)/20:
                grid.populate_entities(Rabbit, 3, self.smart_level, reproduce=True)
    
    @property
    def color(self):
        return WHITE