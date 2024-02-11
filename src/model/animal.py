from model.flora import Plant
class Animal:
    def __init__(self, animal_type, energy):
        self.type = animal_type
        self.energy = energy

    def move(self, grid, old_x, old_y, new_x, new_y):
        if grid.update_count % (grid.size // grid.speed) == 0:
            new_cell = grid.cells[new_x][new_y]
            if isinstance(new_cell.element, self.food_type):
                self.eat()
                new_cell.set_element(Plant())  # supprime la nourriture mangée
            new_cell.set_element(self)  # bouger l'animal vers la nv case
            grid.cells[old_x][old_y].set_element(Plant())

    def eat(self):
        self.energy += self.eat_energy
