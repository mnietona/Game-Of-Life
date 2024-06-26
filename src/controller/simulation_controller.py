import pygame
from model.simulation import Simulation
from view.simulation_view import SimulationView

class SimulationController:
    def __init__(self, app, grid_size, speed, smart_level_fox, smart_level_rabbit, default_carrot_spawn, default_rabbits=None, default_foxes=None):
        self.app = app
        self.model = Simulation(grid_size, speed, smart_level_fox, smart_level_rabbit, default_carrot_spawn, default_rabbits, default_foxes)
        self.view = None
        self.paused = False
        self.i = None
        self.j = None

    def activate(self):
        if self.view is None:
            self.view = SimulationView(self.app.screen, self.model.grid, self.model)
        self.view.reset_click_states() 
        self.view.init_values()
        self.view.show_widgets()  
        self.view.hide_widgets_except()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)
        
        self.view.handle_event(event) 
        if self.i and self.j:
            self.add_or_remove_entity(self.i, self.j) 
        self.update_view_from_model()
        self.view.reset_click_states()
        
    def handle_mouse_click(self, position):
        i, j = self.get_cell_indices(position[0], position[1])
        if self.is_valid_cell(i, j):
            self.view.selected_cell = (i, j)
            self.update_view_add_remove(i, j)
            self.i = i
            self.j = j
    
    def update_view_from_model(self):
        if self.view.back_clicked:
            self.view.hide_widgets()
            self.app.switch_controller("welcome")
        elif self.view.pause_play_clicked:
            self.toggle_pause() 
            self.view.update_buttons_based_on_pause_state(self.paused)
        elif self.view.next_step_clicked:
            self.next_step()
        elif self.view.graph_clicked:
            self.graph_clicked()
    
    def update_view_add_remove(self, i, j):
        add, add_not_all = self.model.grid.possible_add_entity(i, j)
        self.view.add_view = add or add_not_all
        remove = self.model.grid.possible_remove_entity(i, j)
        self.view.show_hide_add_remove_buttons(add, remove, add_not_all)
    
    def add_or_remove_entity(self, i, j):
        
        if self.view.get_add_clicked():
            choice = self.view.get_selected_entity() 
            entity_choice = self.model.grid.get_entity(choice) 
            self.model.grid.add_entity(entity_choice, (i, j))
            self.update_view_add_remove(i, j)
        elif self.view.remove_clicked:
            self.model.grid.remove_element(i, j)
            self.update_view_add_remove(i, j)
        self.model.update_count_population()

    def toggle_pause(self):
        self.paused = not self.paused

    def is_paused(self):
        return self.paused
        
    def next_step(self):
        self.paused = True
        self.model.update_system(force_update=True)
        self.view.update_buttons_based_on_pause_state(self.paused)
        self.view.update_data_and_graph(self.model.turn, self.model.count_rabbits, self.model.count_foxes, self.model.count_carrots)

    def graph_clicked(self):
        self.view.generate_graph()
        
    def get_cell_indices(self, x, y):
        cell_size = self.view.cell_size
        i = (y - 10) // cell_size
        j = (x - 10) // cell_size
        return i, j

    def is_valid_cell(self, i, j):
        return 0 <= i < self.model.grid.size and 0 <= j < self.model.grid.size
    
    def update_widget_view(self):
        self.view.turn = self.model.turn
        self.view.count_rabbit = self.model.count_rabbits
        self.view.count_fox = self.model.count_foxes
        self.view.count_carrot = self.model.count_carrots
        speed = self.view.get_slider_value('speed')
        carrot_spawn_speed = self.view.get_slider_value('carrot_spawn_speed')
        smart_level_rabbit = self.view.get_slider_value('smart_rabbit')
        smart_level_fox = self.view.get_slider_value('smart_fox')
        self.model.set_speed(speed)
        self.model.set_carrot_spawn_speed(carrot_spawn_speed)
        self.model.set_smart_level(smart_level_rabbit, smart_level_fox)

    def render(self):
        
        if not self.is_paused():
            self.model.update_system()
            self.view.update_data_and_graph(self.model.turn, self.model.count_rabbits, self.model.count_foxes, self.model.count_carrots)
        
        if self.view.selected_cell:
            i, j = self.view.selected_cell
            info = self.model.grid.get_cell_info(i, j)
            self.view.selected_cell_info = f"Case ({i}, {j}) : {info}"
        
        self.update_widget_view()
        
        self.view.render()
    
    def resize_screen(self, width, height):
        self.view.resize_screen(width, height)