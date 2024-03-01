import random
from constants import *

class Fauna:
    def __init__(self, grid_size, health, radius, delta):
        self.health = health
        self.radius = max(radius, round(grid_size / 10)) + delta
        self.age = 0
        
    def get_info(self):
        return f"{self.__class__.__name__}- Santé: {int(self.health)}- Age: {self.age}"

    def update(self, i, j, env):
        grid = env.grid
        self.age += 1
        # Le bouge et update pos
        new_position = self.move(i, j, grid)
        self.update_position(i, j, new_position, grid)
        
        # interagie avec l'environnement
        new_i, new_j = new_position
        self.interact_with_environment(new_i, new_j, grid)
        
        # enleve si mort
        self.remove_if_dead(new_i, new_j, grid)

    def is_alive(self):
        return self.health > 0
    
    def remove_if_dead(self, i, j, grid):
        if not self.is_alive():
            grid.remove_element(i, j)

    def update_position(self, i, j, new_position, grid):
        grid.update_entity_position((i, j), new_position)

    def move(self, i, j, grid):
        target_position = grid.find_nearest_target((i, j), self.radius, self.prey)
        if target_position:
            return self.move_towards((i, j), target_position, grid)
        else:
            return self.move_randomly(i, j, grid)
    
    def move_towards(self, current_position, target_position, grid):
        possible_moves = self.get_possible_moves(current_position, grid)
        chosen_move = self.choose_closest_move(possible_moves, target_position)
        return chosen_move if chosen_move else current_position
    
    def move_randomly(self, i, j, grid):
        valid_moves = self.get_valid_moves((i, j), grid)
        return random.choice(valid_moves) if valid_moves else (i, j)

    def choose_closest_move(self, moves, target_position):
        if not moves:
            return None
        return min(moves, key=lambda move: self.calculate_distance(move, target_position))
    
    def calculate_distance(self, position, target_position):
        px, py = position
        tx, ty = target_position
        return abs(px - tx) + abs(py - ty)

    def get_possible_moves(self, position, grid):
        i, j = position
        return [(i + di, j + dj) for di, dj in MOVES if grid.is_cell_valid(i + di, j + dj)]

    def get_valid_moves(self, position, grid):
        return [move for move in self.get_possible_moves(position, grid)]

    def interact_with_environment(self, i, j, grid):
        # Methode a surcharger dans les classes filles
        pass