import random
from constants import *
class Fauna:
    def __init__(self, health_level, radius):
        self.health_level = health_level
        self.radius = radius

    def get_info(self):
        return f"{self.__class__.__name__}- Niveau de vie: {self.health_level}"
    
    def update(self, i, j, grid):
        
        position = (i, j)
        self.health_level -= 1  
        if self.health_level <= 0:
            grid.remove_element(i, j)  
        else:
            new_position = self.move(i, j, grid)  
            self.eat_if_possible(new_position, grid)
            grid.update_entity_position(position, new_position)
        

    def move(self, i, j, grid):
        position = (i, j)
        
        target_position = grid.find_nearest_target(position, self.radius, self.target_type)

        if target_position:
            return self.move_towards(position, target_position, grid)
        else:
            return  self.move_randomly(i, j, grid)
    
    def move_towards(self, current_position, target_position, grid, flee=False):
        i, j = current_position
        target_i, target_j = target_position
        entity = grid.entity_positions.get(current_position)
        entity_type = type(entity) if entity else None

        possible_moves = [
            (i-1, j-1), (i-1, j), (i-1, j+1),
            (i, j-1),             (i, j+1),
            (i+1, j-1), (i+1, j), (i+1, j+1)
        ]
        
        valid_moves = [move for move in possible_moves if grid.is_cell_valid(*move, entity_type)]

        if not valid_moves:
            return current_position
        if flee:
            closest_move = max(valid_moves, key=lambda move: (move[0] - target_i)**2 + (move[1] - target_j)**2)
        else:
            closest_move = min(valid_moves, key=lambda move: (move[0] - target_i)**2 + (move[1] - target_j)**2)

        return closest_move


    def move_randomly(self, i, j, grid):
        current_position = (i, j)
        moves = MOVES 
        valid_moves = []

        for move in moves:
            new_i, new_j = i + move[0], j + move[1]
            if grid.is_cell_valid(new_i, new_j):
                valid_moves.append((new_i, new_j))

        if valid_moves:
            new_position = random.choice(valid_moves)
            grid.update_entity_position(current_position, new_position)
            return new_position
        else:
            return current_position
    
    def eat_if_possible(self, position, grid):
        entity_at_new_position = grid.entity_positions.get(position)
        if entity_at_new_position and isinstance(entity_at_new_position, grid.get_entity(self.target_type)):
            self.health_level += entity_at_new_position.health_level 