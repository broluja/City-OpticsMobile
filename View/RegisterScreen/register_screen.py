from email_validator import validate_email, EmailNotValidError

from kivymd.uix.screen import MDScreen

from View.Managers.http_manager import http_manager
from View.Managers.notification_manager import NotificationManager


class RegisterScreenView(MDScreen):
    """ Screen for logging users. """

    def __init__(self, **kwargs):
        super(RegisterScreenView, self).__init__(**kwargs)
        self.notifier = NotificationManager()
        self.http_manager = http_manager

    def register(self):
        email = self.ids.email.text
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            self.notifier.notify(str(e), background=[1, 0, 0, .7])
            return
        username = self.ids.username.text
        password_one = self.ids.password.text
        password_two = self.ids.password2.text
        if password_one != password_two:
            self.notifier.notify('Make sure two passwords match!')
            return
        self.http_manager.register_user(email, username, password_one, password_two, self.on_success, self.error)

    def error(self, response):
        self.notifier.notify(response)

    def on_success(self, response):
        if isinstance(response.get('username'), list):
            self.notifier.notify(response.get('username')[0], background=[1, 0, 0, .7])
            return
        self.notifier.notify(response.get('response'))
        self.clear()

    def clear(self):
        for item in self.ids.values():
            item.text = ""
