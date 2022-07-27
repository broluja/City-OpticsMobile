from kivymd.uix.screen import MDScreen

from View.Managers.http_manager import http_manager
from View.Managers.notification_manager import NotificationManager


class LoginScreenView(MDScreen):
    """ Screen for logging users. """

    def __init__(self, **kwargs):
        super(LoginScreenView, self).__init__(**kwargs)
        self.notifier = NotificationManager()

    def clear_text(self):
        for widget in self.ids.values():
            widget.text = ''

    def login(self):
        user = self.ids.username.text
        password = self.ids.password.text
        if not user:
            self.notifier.notify('Username field should not be empty.')
            return
        if not password:
            self.notifier.notify('Please provide password.')
            return
        http_manager.user_login(user, password, self.enter, self.error)

    def enter(self, token: str):
        """ Clearing text fields and storing token on App before switching to Main Screen. """
        self.manager.app.token = token
        self.clear_text()
        self.manager.switch_screen('main')

    def error(self, response):
        self.notifier.notify(response, background=[1, 0, 0, .7])
