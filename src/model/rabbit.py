import random
from model.flora import Plant, Carrot
from model.animal import Animal
class Rabbit(Animal):
    def __init__(self):
        super().__init__("Rabbit", 100)
        self.last_reproduction_energy = 100
        self.energy_to_reproduce = 150
        self.group = [self]  # Un groupe de lapins
        self.food_type = Carrot


    def update(self, grid, x, y):
        self.energy -= 1
        if self.energy <= 0:
            grid.rabbit_count -= 1
            self.die(grid, x, y)
            return


        #self.update_group(grid, x, y)

        if random.random() < self.reproduction_rate:
            print("reproduce")
            self.reproduce(grid)

        best_move = self.find_best_move(grid, x, y)
        if best_move:
            for rabbit in self.group:
                rabbit.move(grid, x, y, *best_move)

    def update_group(self, grid, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < grid.size and 0 <= new_y < grid.size:
                cell = grid.cells[new_x][new_y]
                if isinstance(cell.element, Rabbit) and cell.element is not self:
                    self.join_group(cell.element)

    def join_group(self, other_rabbit):
        pass
        """if other_rabbit not in self.group:
            self.group += other_rabbit.group
            self.group = list(set(self.group)) 
            for rabbit in self.group:
                rabbit.group = self.group  # Mettre à jour le groupe pour tous les membres
                rabbit.energy += self.energy  # Partager l'énergie"""

    def find_best_move(self, grid, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        best_move = None
        valid_moves = [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < grid.size and 0 <= y + dy < grid.size and not isinstance(grid.cells[x + dx][y + dy].element, Rabbit)]
        if valid_moves:
            best_move = random.choice(valid_moves)

        return best_move

    def distance_to_closest_carrot(self, grid, x, y):
        # Distance de manhattan à la carotte la plus proche
        best_distance = grid.size * 2
        for i in range(grid.size):
            for j in range(grid.size):
                if isinstance(grid.cells[i][j].element, Carrot):
                    distance = abs(i - x) + abs(j - y)
                    if distance < best_distance:
                        best_distance = distance
        return best_distance


    def reproduce(self, grid):
        
        free_cells = [(i, j) for i in range(grid.size) for j in range(grid.size) if isinstance(grid.cells[i][j].element, Plant)]

        if free_cells:
            new_x, new_y = random.choice(free_cells)
            if grid.rabbit_count <= grid.max_rabbits:
                new_rabbit = Rabbit()
                grid.rabbit_count += 1
                grid.cells[new_x][new_y].set_element(new_rabbit)
    def eat(self,grid):
        self.energy += 10

    def die(self, grid, x, y):

        if isinstance(grid.cells[x][y].element, Rabbit):
            print('dead rabbit')
            grid.cells[x][y].set_element(Plant())
    
