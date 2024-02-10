from model.flora import Plant
from model.rabbit import Rabbit
import random

class Fox:
    def __init__(self):
        self.type = "Fox"
        self.energy = 1000
        self.perception_radius = 5  # Adjust the perception radius as needed

    def update(self, grid, x, y):
        """self.energy -= 0.5
        if self.energy <= 0:
            self.die(grid, x, y)
            return"""

        closest_rabbit = self.find_closest_rabbit(grid, x, y)
        if closest_rabbit:
            new_x, new_y = closest_rabbit
            self.move(grid, x, y, new_x, new_y)
        else:
            # If no rabbit is found, move randomly"""
            self.random_move(grid, x, y)
        print("Fox position after random move:", x, y)

    def random_move(self, grid, x, y):
        empty_cells = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < grid.size and 0 <= new_y < grid.size:
                if grid.cells[new_x][new_y].element.type =="Plant":
                    empty_cells.append((new_x, new_y))
                    print(" AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print("Empty cells:", empty_cells)

        if empty_cells:
            new_x, new_y = random.choice(empty_cells)
            print("Selected new position:", new_x, new_y)
            self.move(grid, x, y, new_x, new_y)

    def find_closest_rabbit(self, grid, x, y):
        best_distance = self.perception_radius + 1  # Initialize with a distance greater than the perception radius
        closest_rabbit = None

        for i in range(max(0, x - self.perception_radius), min(grid.size, x + self.perception_radius + 1)):
            for j in range(max(0, y - self.perception_radius), min(grid.size, y + self.perception_radius + 1)):
                if isinstance(grid.cells[i][j].element, Rabbit):
                    distance = abs(x - i) + abs(y - j)
                    if distance < best_distance:
                        best_distance = distance
                        closest_rabbit = (i, j)

        return closest_rabbit

    def move(self, grid, old_x, old_y, new_x, new_y):
        if grid.update_count % (grid.size // grid.speed) == 0:

            new_cell = grid.cells[new_x][new_y]
            print("Moving fox from", old_x, old_y, "to", new_x, new_y)
            if isinstance(new_cell.element, Rabbit):
                self.eat()
                new_cell.set_element(Plant())  # The rabbit is eaten

            # Set the new cell with the current fox object
            new_cell.set_element(self)
            grid.cells[old_x][old_y].set_element(Plant())

    def eat(self):
        self.energy += 20

    def die(self, grid, x, y):
        grid.cells[x][y].set_element(Plant())