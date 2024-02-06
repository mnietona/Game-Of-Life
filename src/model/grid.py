class Grid:
    def __init__(self, size):
        self.size = size
        self.cells = [[0 for _ in range(size)] for _ in range(size)]
