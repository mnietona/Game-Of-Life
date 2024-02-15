from model.grid import Grid  
from view.grid_view import GridView 

class GridController:
    def __init__(self, app):
        self.app = app
        self.model = Grid(50, 5) # A moddif
        self.view = None

    def activate(self):
        if self.view is None:
            self.view = GridView(self.app.screen, self.model)
        self.view.reset_button_clicks() 
        self.view.show_widgets()  


    def handle_event(self, event):
        self.view.handle_event(event)  

        if self.view.back_clicked:
            self.view.hide_widgets()
            self.app.switch_controller("welcome")
            self.view.reset_button_clicks()  
        elif self.view.pause_play_clicked:
            self.is_paused()
            self.view.reset_button_clicks()
        elif self.view.next_step_clicked:
            self.next_step()
            self.view.reset_button_clicks()

    def is_paused(self):
        pass
        
    def next_step(self):
       pass

    def get_cell_indices(self, x, y):
        cell_size = self.view.cell_size
        i = (y - 10) // cell_size
        j = (x - 10) // cell_size
        return i, j

    def is_valid_cell(self, i, j):
        return 0 <= i < self.model.size and 0 <= j < self.model.size

    def render(self):
        self.view.render()
