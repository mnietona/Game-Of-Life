from model.elements import Element
class Terrain(Element):
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

class Plaine(Terrain):
    def __init__(self, temperature, humidity):
        super().__init__(temperature, humidity)

    
