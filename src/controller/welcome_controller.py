from view.welcome_view import WelcomeView

class WelcomeController:
    def __init__(self, app):
        self.app = app
        self.view = WelcomeView(app.screen)

    def activate(self):
        self.view.show_widgets()
        self.view.reset_start_clicked()

    def handle_event(self, event): 
        self.view.handle_event(event)
        if self.view.start_clicked:
            self.start_game()
            self.view.reset_start_clicked()

    def start_game(self):
        grid_size = self.view.get_grid_size()
        speed = self.view.get_speed()
        self.view.hide_widgets()
        self.app.switch_controller("grid", grid_size, speed)

    def render(self):
        self.view.render()
