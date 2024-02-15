from model.flora import Plante
class Cell:
    def __init__(self):
        self.element = Plante()

    def set_element(self, element):
        self.element = element
    
    def get_info(self):
        return self.element.get_info()

    def update(self):
        if self.element is not None:
            result = self.element.update()
            if result is not None:
                self.set_element(result)
