class Flora:
    def __init__(self, lifespan):
        self.lifespan = lifespan

    def get_info(self):
        if self.lifespan == float('inf'):
            return f"Flore: {self.__class__.__name__}- Durée de vie: éternelle"
        
        return f"Flore: {self.__class__.__name__}- Durée de vie: {self.lifespan}"

    def update(self, i, j, grid): 
        if self.lifespan > 0:
            self.lifespan -= 1
        else:
            grid.remove_element(i, j)
     
    @property
    def color(self):
        return (255, 255, 255)  # White

class Plant(Flora):
    def __init__(self, lifespan=float('inf')):
        super().__init__(lifespan)
    
    @property
    def color(self):
        return (58, 137, 35)  # Green

class Carrot(Flora):
    def __init__(self, lifespan=50):
        super().__init__(lifespan)
    
    @property
    def color(self):
        return (255, 165, 0)  # Orange
