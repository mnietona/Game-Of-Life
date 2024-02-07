from model.animals import Animal, Fox, Rabbit

class Cell:
    def __init__(self):
        self.element = None  # Ajout d'un attribut pour l'élément

    def set_element(self, element):
        self.element = element

    def info(self):
        return [self.element]

    def update(self):
        if self.element is not None:
            self.element.update()
