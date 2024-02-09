from model.flora import Plant
from model.rabbit import Rabbit

class Fox:
    def __init__(self):
        self.type = "Fox"
        self.energy = 100

    def update(self, grid, x, y):
        self.energy -= 0.5
        if self.energy <= 0:
            self.die(grid, x, y)
            return

        best_move = self.find_closest_rabbit(grid, x, y)
        if best_move:
            new_x, new_y = best_move
            self.move(grid, x, y, new_x, new_y)

    def find_closest_rabbit(self, grid, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        best_distance = self.distance_to_closest_rabbit(grid, x, y)
        best_move = None

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < grid.size and 0 <= new_y < grid.size:
                distance = self.distance_to_closest_rabbit(grid, new_x, new_y)
                if distance < best_distance:
                    best_distance = distance
                    best_move = (new_x, new_y)

        return best_move

    def distance_to_closest_rabbit(self, grid, x, y):
        # Distance de Manhattan à la proie (lapin) la plus proche
        best_distance = grid.size * 2
        for i in range(grid.size):
            for j in range(grid.size):
                if isinstance(grid.cells[i][j].element, Rabbit):
                    distance = abs(x - i) + abs(y - j)
                    if distance < best_distance:
                        best_distance = distance
        return best_distance

    def move(self, grid, old_x, old_y, new_x, new_y):
        new_cell = grid.cells[new_x][new_y]
        if isinstance(new_cell.element, Rabbit):
            self.eat()
            new_cell.set_element(Plant())  # Le lapin est mangé

        if self.is_adjacent_to_fox(grid, new_x, new_y):
            self.energy -= 10  # Perte d'énergie en étant adjacent à un autre renard

        grid.cells[new_x][new_y].set_element(self)
        grid.cells[old_x][old_y].set_element(Plant())

    def is_adjacent_to_fox(self, grid, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            adj_x, adj_y = x + dx, y + dy
            if 0 <= adj_x < grid.size and 0 <= adj_y < grid.size:
                if isinstance(grid.cells[adj_x][adj_y].element, Fox):
                    return True
        return False

    def eat(self):
        self.energy += 20

    def die(self, grid, x, y):
        grid.cells[x][y].set_element(Plant())
