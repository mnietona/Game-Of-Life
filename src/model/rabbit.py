from model.fauna import Fauna
from model.flora import Carrot

class Rabbit(Fauna):
    def __init__(self, health_level=50, radius=7):
        super().__init__(health_level, radius) 
        self.target_type = Carrot
    
    def update(self, i, j, grid):
        super().update(i, j, grid)
    
    @property
    def color(self):
        return (255, 255, 255)  # White
