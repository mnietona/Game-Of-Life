from model.flora import Plant
class Animal:
    def __init__(self, animal_type, energy,reproduction_rate= 0.01): #une chance sur 100 de se reproduire par update
        self.type = animal_type
        self.energy = energy
        self.reproduction_rate = reproduction_rate

    def move(self, grid, old_x, old_y, new_x, new_y):
        if grid.update_count % (grid.size // grid.speed) == 0:
            new_cell = grid.cells[new_x][new_y]
            if isinstance(new_cell.element, self.food_type):
                self.eat(grid)
                new_cell.set_element(Plant())  # supprime la nourriture mangée
            if new_cell.element.type == "Plant":
                new_cell.set_element(self)  # bouger l'animal vers la nv case
                grid.cells[old_x][old_y].set_element(Plant())

    def eat(self, grid):
        self.energy += 10
    
    def get_info(self):
        return f"{self.type} energy: {self.energy}"
