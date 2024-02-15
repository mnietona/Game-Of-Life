from model.fauna import Fauna

class Rabbit(Fauna):
    def __init__(self, health_level=50, radius=5, grid=None):
        super().__init__(health_level, radius)
        self.grid = grid 
    
    def update(self, i, j, grid):
        super().update(i, j, grid)
    
    @property
    def color(self):
        return (255, 255, 255)  # White
