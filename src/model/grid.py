from model.cell import Cell

class Grid:
    def __init__(self, size, speed):
        self.size = size
        self.speed = speed
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]

    def udpate_systeme(self):
        for i in range(self.size):
            for j in range(self.size):
                self.cells[i][j].update()