from model.elements import Element
from model.plantes import Plante

class Animal(Element):
    def __init__(self, name):
        self.food = None 
        self.satiete = 100
        self.direction = None
        self.position = None
        
    def move(self):
        print("I am moving")
    
    def eat(self):
        print("I am eating")
        
class Rabbit(Animal):
    
    def __init__(self, name):
        super().__init__(name)
        self.food = Plante
        print("I am a rabbit")
        print("My name is", self.name)
    
    def move(self):
        # la case qui mene a manger  -> plante 
        print("I am jumping")
    
    def eat(self):
        print("I am eating grass")
        

class Fox(Animal):
    
    def __init__(self, name):
        super().__init__(name)
        self.food = Rabbit
        print("I am a fox")
        print("My name is", self.name)
        
    def move(self):
        # la case qui mene a manger -> lapin
        print("I am moving fast")
        
    def eat(self):
        print("I am eating rabbits")
