from src.model.flora import Plant

class Cell:
    def __init__(self):
        self.element = Plant()  # Par défaut chaque cell a plante

    def set_element(self, element):
        self.element = element

    def info(self):
        return [self.element.type]

    def update(self):
        if self.element is not None:
            self.element.update()
