from view.setting_view import SettingView

class SettingController:
    def __init__(self, app):
        self.app = app
        self.view = None
        self.grid_size = None
        
    def activate(self):
        if self.view is None:
            self.view = SettingView(self.app.screen)
        self.view.init_ui_elements(self.grid_size)
        self.view.show_widgets()
        self.view.reset_clicked()

    def handle_event(self, event): 
        self.view.handle_event(event)
        if self.view.back_menu_clicked:
            self.back_menu()
            self.view.reset_clicked()

    def back_menu(self):
        self.view.hide_widgets()
        smart_rabbit = self.view.get_slider_value("smart_rabbit")
        smart_fox = self.view.get_slider_value("smart_fox")
        start_rabbit = self.view.get_slider_value("start_rabbit")
        start_fox = self.view.get_slider_value("start_fox")
        spawn_carrot = self.view.get_slider_value("spawn_carrot")
        self.app.switch_controller("welcome")
        self.app.current_controller.update_settings(smart_rabbit, smart_fox, start_rabbit, start_fox, spawn_carrot)
    
    def update_settings(self, grid_size):
        self.grid_size = grid_size

    def resize_screen(self, width, height):
        self.view.resize_screen(width, height)

    def render(self):
        self.view.render()