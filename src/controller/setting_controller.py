from view.setting_view import SettingView

class SettingController:
    def __init__(self, app):
        self.app = app
        self.view = None


    def activate(self):
        if self.view is None:
            self.view = SettingView(self.app.screen)
        self.view.show_widgets()
        self.view.reset_clicked()

    def handle_event(self, event): 
        self.view.handle_event(event)
        if self.view.back_menu_clicked:
            self.back_menu()
            self.view.reset_clicked()

    def back_menu(self):
        self.view.hide_widgets()
        self.app.switch_controller("welcome")

    def render(self):
        self.view.render()