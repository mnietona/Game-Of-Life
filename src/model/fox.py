class Fox:
    def __init__(self):
        self.type = "Fox"
        self.energy = 100  

    def update(self):
        self.energy -=-0.5  
        if self.energy <= 0:
            self.die()

    def eat(self, rabbit):
        self.energy += 10

    def die(self):
        ...
