import time

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen

from View.Managers.http_manager import http_manager
from View.Managers.notification_manager import NotificationManager


class MainScreenView(MDScreen):
    """ Main App Screen. """
    data = {  # Options on SpeedDial Button
        'Appointments': 'clock-outline',
        'Products': 'glasses',
        'Orders': 'book-clock',
        'Customers': 'face-agent',
        'Messages': 'message-text-lock',
        'Back': 'keyboard-backspace'
    }

    def __init__(self, **kwargs):
        super(MainScreenView, self).__init__(**kwargs)
        self.http_manager = http_manager
        self.notifier = NotificationManager()
        Clock.schedule_interval(self.get_time, 1)

    def get_time(self, *args):
        """ Providing time string for time Label. """
        self.ids.time.text = time.asctime()

    def on_server_rejection(self, data):
        if isinstance(data, dict):
            self.notifier.notify('You do not have required permissions!', background=[1, 0, 0, .7], duration=4.0)
            return True
        return False

    def callback(self, instance):
        token = self.manager.app.token
        if instance.icon == 'clock-outline':
            data = self.http_manager.get_data('appointments', token)
            self.manager.app.data = data
            if self.on_server_rejection(data):
                return
            self.manager.switch_screen('appointments')
        elif instance.icon == 'glasses':
            data = self.http_manager.get_data('products', token)
            self.manager.app.data = data
            if self.on_server_rejection(data):
                return
            self.manager.switch_screen('products')
        elif instance.icon == 'book-clock':
            data = self.http_manager.get_data('orders', token)
            self.manager.app.data = data
            if self.on_server_rejection(data):
                return
            self.manager.switch_screen('orders')
        elif instance.icon == 'face-agent':
            data = self.http_manager.get_data('customers', token)
            self.manager.app.data = data
            if self.on_server_rejection(data):
                return
            self.manager.switch_screen('customers')
        elif instance.icon == 'message-text-lock':
            data = self.http_manager.get_data('messages', token)
            self.manager.app.data = data
            if self.on_server_rejection(data):
                return
            self.manager.switch_screen('messages')
        elif instance.icon == 'keyboard-backspace':
            self.manager.switch_screen('login')
            self.manager.app.token = None
