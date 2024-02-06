class Cell:
    def __init__(self, temperature):
        self.temperature = temperature
        self.humidity = 0
    
    def info(self):
        return [self.temperature, self.humidity]