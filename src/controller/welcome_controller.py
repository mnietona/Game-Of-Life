from view.welcome_view import WelcomeView

class WelcomeController:
    def __init__(self, app):
        self.app = app
        self.view = WelcomeView(app.screen)

    def activate(self):
        # Réinitialise l'état de la vue si nécessaire
        self.view.reset_start_clicked()

    def handle_event(self, event):
        # Gère les événements et les transmet à la vue
        self.view.handle_event(event)
        # Vérifie si le bouton de démarrage a été cliqué
        if self.view.start_clicked:
            self.start_game()
            self.view.reset_start_clicked()

    def start_game(self):
        # Logique pour démarrer le jeu, par exemple changer de vue
        self.app.switch_controller("grid")

    def render(self):
        # Dessine la vue
        self.view.render()
