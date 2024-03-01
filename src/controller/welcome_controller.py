from view.welcome_view import WelcomeView

class WelcomeController:
    def __init__(self, app):
        self.app = app
        self.view = None
        self.grid_size = 40
        self.smart_level_rabbit = 1
        self.smart_level_fox = 1
        self.default_rabbits = None
        self.default_foxes = None
        self.default_carrot_spawn = 1

    def activate(self):
        if self.view is None:
            self.view = WelcomeView(self.app.screen)
        self.view.resize_screen(self.app.screen.get_width(), self.app.screen.get_height())
        self.view.show_widgets()
        self.view.reset_clicked()

    def handle_event(self, event): 
        self.view.handle_event(event)
        
        if self.view.start_clicked:
            self.start_game()
            self.view.reset_clicked()
        elif self.view.setting_clicked:
            self.show_settings_window()
            self.view.reset_clicked()
    
    def update_settings(self, smart_rabbit, smart_fox, start_rabbit, start_fox, spawn_carrot):
        self.smart_level_rabbit = smart_rabbit
        self.smart_level_fox = smart_fox
        self.default_rabbits = start_rabbit
        self.default_foxes = start_fox
        self.default_carrot_spawn = spawn_carrot

    def start_game(self):
        grid_size = self.view.get_grid_size()
        if self.grid_size != grid_size:
            self.default_rabbits = None
            self.default_foxes = None
        speed = self.view.get_speed()
        self.view.hide_widgets()
        self.view.set_initial_values()
        self.app.switch_controller("grid", grid_size, speed, self.smart_level_rabbit, self.smart_level_fox, self.default_carrot_spawn, self.default_rabbits, self.default_foxes)
    
    def show_settings_window(self):
        self.view.hide_widgets()
        self.grid_size = self.view.get_grid_size()
        self.view.set_initial_values()
        self.app.switch_controller("setting", self.grid_size)
        
    def resize_screen(self, width, height):
        self.view.resize_screen(width, height)

    def render(self):
        self.view.render()