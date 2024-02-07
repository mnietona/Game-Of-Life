import random
from src.model.flora import Plant, Carrot

class Rabbit:
    def __init__(self):
        self.type = "Rabbit"
        self.energy = 100
        self.last_reproduction_energy = 100
        self.group = [self]  # Un groupe de lapins

    def update(self, grid, x, y):
        self.energy -= 0.5
        if self.energy <= 0:
            self.die(grid, x, y)
            return

        self.update_group(grid, x, y)
        
        if self.energy >= self.last_reproduction_energy + 100:
            self.reproduce(grid)
            self.last_reproduction_energy = self.energy

        # Si le groupe a plus de trois membres, un lapin se sépare
        if len(self.group) > 3:
            self.group.remove(self)
            self.group = [self]  # Retourne à un groupe solo

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
        if other_rabbit not in self.group:
            self.group += other_rabbit.group
            self.group = list(set(self.group)) 
            for rabbit in self.group:
                rabbit.group = self.group  # Mettre à jour le groupe pour tous les membres
                rabbit.energy += self.energy  # Partager l'énergie

    def find_best_move(self, grid, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] 
        best_distance = grid.size * 2
        best_move = None

        carrot_found = False
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < grid.size and 0 <= new_y < grid.size and not isinstance(grid.cells[new_x][new_y].element, Rabbit):
                distance = self.distance_to_closest_carrot(grid, new_x, new_y)
                if distance < best_distance:
                    best_distance = distance
                    best_move = (new_x, new_y)
                    carrot_found = True

        # Si aucune carotte n'est trouvée, choisir une direction aléatoire
        if not carrot_found:
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

    def move(self, grid, old_x, old_y, new_x, new_y):
        new_cell = grid.cells[new_x][new_y]
        
        if isinstance(new_cell.element, Carrot):
            self.eat()

        grid.cells[new_x][new_y].set_element(self)
        grid.cells[old_x][old_y].set_element(Plant())
    
    def reproduce(self, grid):
        
        free_cells = [(i, j) for i in range(grid.size) for j in range(grid.size) if isinstance(grid.cells[i][j].element, Plant)]

        if free_cells:
            new_x, new_y = random.choice(free_cells)
            new_rabbit = Rabbit()
            grid.cells[new_x][new_y].set_element(new_rabbit)

    def eat(self):
        self.energy += 10

    def die(self, grid, x, y):
        grid.cells[x][y].set_element(Plant())
    
