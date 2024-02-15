class Flore:
    def __init__(self, duree_de_vie):
        self.duree_de_vie = duree_de_vie

    def get_info(self):
        if self.duree_de_vie == float('inf'):
            return f"Flore: {self.__class__.__name__}- Durée de vie: éternelle"
        
        return f"Flore: {self.__class__.__name__}- Durée de vie: {self.duree_de_vie}"

    def update(self):
        if self.duree_de_vie > 0:
            self.duree_de_vie -= 1
            return None
        else:
            return Plante()
            
    @property
    def color(self):
        return (255, 255, 255)  # Blanc

class Plante(Flore):
    def __init__(self, duree_de_vie=float('inf')):
        super().__init__(duree_de_vie)
    
    @property
    def color(self):
        return (58, 137, 35)  # Vert

class Carotte(Flore):
    def __init__(self, duree_de_vie=50):
        super().__init__(duree_de_vie)
    
    @property
    def color(self):
        return (255, 165, 0)  # Orange
