import pygame
from model.grid import Grid  
from view.grid_view import GridView 

class GridController:
    def __init__(self, app, grid_size, speed):
        self.app = app
        self.model = Grid(grid_size, speed)
        self.view = None
        self.paused = False

    def activate(self):
        if self.view is None:
            self.view = GridView(self.app.screen, self.model)
        self.view.reset_button_clicks() 
        self.view.show_widgets()  

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            i, j = self.get_cell_indices(x, y)
            if self.is_valid_cell(i, j):
                self.view.selected_cell = (i, j)
        
        self.view.handle_event(event)  

        if self.view.back_clicked:
            self.view.hide_widgets()
            self.app.switch_controller("welcome")
            self.view.reset_button_clicks()  
        elif self.view.pause_play_clicked:
            self.toggle_pause() 
            self.view.update_buttons_based_on_pause_state(self.paused)
            self.view.reset_button_clicks()
        elif self.view.next_step_clicked:
            self.next_step()
            self.view.reset_button_clicks()
    
    def toggle_pause(self):
        self.paused = not self.paused

    def is_paused(self):
        return self.paused
        
    def next_step(self):
        self.paused = True
        self.model.update_systeme(force_update=True)
        self.view.update_buttons_based_on_pause_state(self.paused)

    def get_cell_indices(self, x, y):
        cell_size = self.view.cell_size
        i = (y - 10) // cell_size
        j = (x - 10) // cell_size
        return i, j

    def is_valid_cell(self, i, j):
        return 0 <= i < self.model.size and 0 <= j < self.model.size

    def render(self):
        
        if not self.is_paused():
            self.model.update_systeme()
        
        if self.view.selected_cell:
            i, j = self.view.selected_cell
            info = self.model.get_cell_info(i, j)
            self.view.selected_cell_info = f"Case selectionnée  ({i}, {j})- {info}"
        
        self.model.set_speed(self.view.slider_speed.getValue())
        
        self.view.render()