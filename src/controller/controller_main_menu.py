class ControllerMainMenu:
    def __init__(self, view):
        self.view = view

    def handle_event(self, event):
        return self.view.handle_mouse_event(event)
