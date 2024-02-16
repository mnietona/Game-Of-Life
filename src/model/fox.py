from model.fauna import Fauna
from model.rabbit import Rabbit

class Fox(Fauna):
    def __init__(self, health_level=100, radius=5):
        super().__init__(health_level, radius)
        self.target_type = Rabbit
    
    def update(self, i, j, grid):
        super().update(i, j, grid)

    @property
    def color(self):
        return (255, 0, 0)  # Red