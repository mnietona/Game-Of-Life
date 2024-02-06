class Cell:
    def __init__(self, temperature):
        self.temperature = temperature
        self.humidity = 0
        self.vegetation = 0
        self.elevation = 0
        self.is_water = False
        
    
    def info(self):
        return [self.temperature, self.humidity, self.vegetation, self.elevation, self.is_water]
