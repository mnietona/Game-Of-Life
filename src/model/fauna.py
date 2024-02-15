import random
class Fauna:
    def __init__(self, health_level, radius):
        self.health_level = health_level
        self.radius = radius

    def get_info(self):
        return f"{self.__class__.__name__}- Niveau de vie: {self.health_level}"
    
    def update(self, i, j, grid):
        self.health_level -= 1
        if self.health_level <= 0:
            grid.remove_element(i, j)
        else:
            self.move(i, j, grid)
    
    def move(self, i, j, grid):
        # Modif pour aller manger sa nourriture si elle est dans son rayon
        self.move_randomly(i, j, grid)
    
    def move_randomly(self, i, j, grid):
        current_position = (i, j)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # 8 directions possibles
        valid_moves = []

        for move in moves:
            new_i, new_j = i + move[0], j + move[1]
            if 0 <= new_i < grid.size and 0 <= new_j < grid.size and grid.is_cell_valid(new_i, new_j):
                valid_moves.append((new_i, new_j))

        if valid_moves:
            new_position = random.choice(valid_moves)
            grid.update_entity_position(current_position, new_position)
            return new_position
        else:
            return current_position