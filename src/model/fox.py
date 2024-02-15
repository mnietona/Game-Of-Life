from model.fauna import Fauna

class Fox(Fauna):
    def __init__(self, health_level=100, radius=10, grid=None):
        super().__init__(health_level, radius)
        self.grid = grid 
    
    def update(self, i, j, grid):
        super().update(i, j, grid)

    @property
    def color(self):
        return (255, 0, 0)  # Red