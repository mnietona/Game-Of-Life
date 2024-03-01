import random
from constants import *

class Fauna:
    
    def __init__(self, health_level, radius, health_reproduction, reproduction_rate, grid_size, delta):
        self.health = health_level
        self.radius_base = max(radius, round(grid_size / 10)) + delta
        self.radius = self.radius_base
        self.health_reproduction = health_reproduction
        self.reproduction_rate = reproduction_rate
        self.age = 0

    def get_info(self):
        return f"{self.__class__.__name__}- Xp: {self.health},   Age : {self.age}- Rayon : {self.radius} - Taux de reproduction : {self.reproduction_rate * 100}%"
    
    def adjust_radius_based_on_intelligence(self):
        self.radius = self.radius_base * self.smart_level
    
    def set_smart_level(self, smart_level):
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()    
        
    def update(self, i, j, env):
        grid = env.grid
        self.decrease_health()
        if self.is_alive():
            self.perform_actions(i, j, grid)
        else:
            grid.remove_element(i, j)

    def decrease_health(self):
        self.health -= 1
        self.age += 1

    def is_alive(self):
        return self.health > 0

    def perform_actions(self, i, j, grid):
        new_position = self.decide_movement(i, j, grid)
        if new_position:
            self.eat_if_possible(new_position, grid)
            grid.update_entity_position((i, j), new_position)

    def decide_movement(self, i, j, grid):
        target_position = grid.find_nearest_target((i, j), self.radius, self.target_type)
        if target_position:
            return self.move_towards((i, j), target_position, grid)
        else:
            return self.move_randomly(i, j, grid)

    def move_towards(self, current_position, target_position, grid, flee=False):
        possible_moves = self.get_possible_moves(current_position, grid)
        if flee:
            chosen_move = self.choose_furthest_move(possible_moves, target_position)
        else:
            chosen_move = self.choose_closest_move(possible_moves, target_position)

        return chosen_move if chosen_move else current_position

    def move_randomly(self, i, j, grid):
        valid_moves = self.get_valid_moves((i, j), grid)
        return random.choice(valid_moves) if valid_moves else (i, j)

    def get_possible_moves(self, position, grid):
        i, j = position
        entity_type = type(self)
        return [(i + di, j + dj) for di, dj in MOVES if grid.is_cell_valid(i + di, j + dj, entity_type)]

    def get_valid_moves(self, position, grid):
        return [move for move in self.get_possible_moves(position, grid)]

    def choose_closest_move(self, moves, target_position):
        if not moves:
            return None
        return min(moves, key=lambda move: self.calculate_distance(move, target_position))

    def choose_furthest_move(self, moves, target_position):
        if not moves:
            return None
        return max(moves, key=lambda move: self.calculate_distance(move, target_position))

    def calculate_distance(self, position, target_position):
        px, py = position
        tx, ty = target_position
        return abs(px - tx) + abs(py - ty)

    def eat_if_possible(self, position, grid):
        entity_at_new_position = grid.entity_positions.get(position)
        if entity_at_new_position and isinstance(entity_at_new_position, grid.get_entity(self.target_type)):
            self.health += entity_at_new_position.health
    
    def try_reproduce(self, grid):
        if random.random() < self.reproduction_rate:
            grid.populate_entities(type(self), 1, smart_level=self.smart_level, reproduce=True)