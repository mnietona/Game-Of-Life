from model.animal import Animal
from model.rabbit import Rabbit
import random
from model.flora import Plant
class Fox(Animal):
    def __init__(self):
        super().__init__("Fox", 300,0.001)
        self.perception_radius = 7  #distance de perception (si y'a un lapin à cette distance,
        #                            il se dirigera vers celui-ci)
        self.food_type = Rabbit
        self.eat_energy = 20

    def update(self, grid, x, y):
        self.energy -= 1
        if self.energy <= 0:
            grid.fox_count -= 1
            self.die(grid, x, y)
            return

        if random.random() < self.reproduction_rate:
            print("reproduce fox")
            self.reproduce(grid)
            grid.fox_count += 1

        closest_food = self.find_closest_food(grid, x, y)
        if closest_food:
            new_x, new_y = closest_food
            # calcule la direction vers le lapin le plus proche
            dx = 1 if new_x > x else (-1 if new_x < x else 0)
            dy = 1 if new_y > y else (-1 if new_y < y else 0)
            # bouger d'une case vers le lapin
            self.move(grid, x, y, x + dx, y + dy)
        else:
            self.random_move(grid, x, y)

    def random_move(self, grid, x, y):
        empty_cells = [(x + dx, y + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                       if 0 <= x + dx < grid.size and 0 <= y + dy < grid.size
                       and grid.cells[x + dx][y + dy].element.type == "Plant"]
        if empty_cells:
            new_x, new_y = random.choice(empty_cells)
            self.move(grid, x, y, new_x, new_y)

    def find_closest_food(self, grid, x, y):
        best_distance = self.perception_radius + 1  #on commence avec une distance + grande que le rayon de base
        closest_rabbit = None

        # parcours des cellules dans le voisinage du point (x, y)
        for i in range(max(0, x - self.perception_radius), min(grid.size, x + self.perception_radius + 1)):
            for j in range(max(0, y - self.perception_radius), min(grid.size, y + self.perception_radius + 1)):
                if isinstance(grid.cells[i][j].element, self.food_type):
                    distance = abs(x - i) + abs(y - j)  # calcul distance Manhattan
                    if distance < best_distance:
                        best_distance = distance
                        closest_rabbit = (i, j)

        return closest_rabbit

    def reproduce(self, grid):
        free_cells = [(i, j) for i in range(grid.size) for j in range(grid.size) if
                      isinstance(grid.cells[i][j].element, Plant)]

        if free_cells:
            new_x, new_y = random.choice(free_cells)
            new_fox = Fox()
            grid.cells[new_x][new_y].set_element(new_fox)

    def eat(self,grid):
        print("rabbit eated by a fox")
        self.energy += 20
        grid.rabbit_count -= 1

    def die(self, grid, x, y):
        print("dead fox")
        grid.cells[x][y].set_element(Plant())