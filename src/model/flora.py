class Plant:
    def __init__(self):
        self.type = "Plant"

    def update(self):
        pass
    
    def get_info(self):
        return self.type
    
class Carrot:
    def __init__(self, energy=50):
        self.type = "Carrot"
        self.energy = energy
    def update(self):
        pass

    def get_info(self):
        return f"{self.type} energy: {self.energy}"
