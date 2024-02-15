from model.flora import Plant

class Cell:
    def __init__(self):
        self.element = Plant()  # Par défaut chaque cell a plante

    def set_element(self, element):
        self.element = element
    
    def get_info(self):
        return self.element.get_info()

    def update(self):
        if self.element is not None:
            self.element.update()
