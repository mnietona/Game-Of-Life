from view.welcome_view import WelcomeView

class WelcomeController:
    def __init__(self, app):
        self.app = app
        self.view = WelcomeView(app.screen)

    def activate(self):
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

    def start_game(self):
        grid_size = self.view.get_grid_size()
        speed = self.view.get_speed()
        smart_level_rabbit = 3
        smart_level_fox = 1
        self.view.hide_widgets()
        self.app.switch_controller("grid", grid_size, speed, smart_level_rabbit, smart_level_fox)
    
    def show_settings_window(self):
        self.view.hide_widgets()
        self.app.switch_controller("setting")
    
    def resize_screen(self, width, height):
        self.view.resize_screen(width, height)

    def render(self):
        self.view.render()