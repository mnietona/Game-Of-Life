import random
from constants import *

class Fauna:
    def __init__(self, grid_size, health, radius, delta):
        self.health = health
        self.radius_base = max(radius, round(grid_size / 10)) + delta
        self.radius = self.radius_base
        self.age = 0
        
    def get_info(self):
        return f"{self.__class__.__name__}- Santé: {int(self.health)}, Age: {self.age}- Rayon: {int(self.radius)}"
    
    def adjust_radius_based_on_intelligence(self):
        self.radius = self.radius_base * self.smart_level
    
    def set_smart_level(self, smart_level):
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence() 

    def update(self, i, j, env):
        grid = env.grid
        self.age += 1
        new_position = self.interact_with_environment(i, j, grid)
        self.update_position_if_alive(i, j, new_position, grid)

    def is_alive(self):
        return self.health > 0
    
    def update_position_if_alive(self, i, j, new_position, grid):
        if not self.is_alive():
            grid.remove_element(i, j)
        else:
            self.update_position(i, j, new_position, grid)

    def update_position(self, i, j, new_position, grid):
        grid.update_entity_position((i, j), new_position)

    def move(self, i, j, grid):
        target_position = grid.find_nearest_target((i, j), self.radius, self.target_type)
        if target_position:
            return self.move_towards((i, j), target_position, grid)
        else:
            return self.move_randomly(i, j, grid)
    
    def move_towards(self, current_position, target_position, grid):
        possible_moves = self.get_possible_moves(current_position, grid)
        random.shuffle(possible_moves)
        chosen_move = self.choose_closest_move(possible_moves, target_position, grid)
        return chosen_move if chosen_move else current_position
    
    def move_randomly(self, i, j, grid):
        valid_moves = self.get_valid_moves((i, j), grid)
        random.shuffle(valid_moves)
        return random.choice(valid_moves) if valid_moves else (i, j)

    def choose_closest_move(self, moves, target_position, grid):
        if not moves:
            return None
        return min(moves, key=lambda move: grid.calculate_distance(move, target_position))

    def get_possible_moves(self, position, grid):
        i, j = position
        return [(i + di, j + dj) for di, dj in MOVES if grid.is_cell_valid(i + di, j + dj, entity_type=self.__class__)]

    def get_valid_moves(self, position, grid):
        return [move for move in self.get_possible_moves(position, grid)]

    def interact_with_environment(self, i, j, grid):
        pass # To be implemented by subclasses
    
    def after_interaction(self, new_position, grid):
        self.health -= 1
        if self.try_to_eat(new_position, grid):
            self.try_reproduce(grid) 
    
    def try_to_eat(self, new_position, grid):
        if new_position in grid.entity_positions:
            entity = grid.entity_positions[new_position]
            if isinstance(entity, grid.get_entity(self.target_type)):
                self.health += entity.health
                grid.remove_element(new_position[0], new_position[1])
                return True
        return False
