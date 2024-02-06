from model.cell import Cell

class Grid:
    def __init__(self, size, temperature):
        self.size = size
        self.temperature = temperature
        self.cells = [[Cell(self.temperature) for _ in range(size)] for _ in range(size)]