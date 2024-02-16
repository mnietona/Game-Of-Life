class Flora:
    def __init__(self, health_level):
        self.health_level = health_level

    def get_info(self):
        if self.health_level == float('inf'):
            return f"Flore: {self.__class__.__name__}- Durée de vie: éternelle"
        
        return f"Flore: {self.__class__.__name__}- Durée de vie: {self.health_level}"

    def update(self, i, j, grid): 
        if self.health_level > 0:
            self.health_level -= 1
        else:
            grid.remove_element(i, j)
     
    @property
    def color(self):
        return (0, 0, 0) # Black

class Plant(Flora):
    def __init__(self, health_level=float('inf')):
        super().__init__(health_level)
    
    @property
    def color(self):
        return (58, 137, 35)  # Green

class Carrot(Flora):
    def __init__(self, health_level=50):
        super().__init__(health_level)
    
    @property
    def color(self):
        return (255, 165, 0)  # Orange
