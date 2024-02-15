from model.flora import Plant
class Cell:
    def __init__(self):
        self.element = Plant()  

    def set_element(self, element):
        self.element = element
    
    def get_info(self):
        return self.element.get_info()

    def update(self, i, j, grid): 
        self.element.update(i, j, grid)
            