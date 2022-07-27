from json import JSONEncoder
import textwrap

from kivy.properties import ObjectProperty, ListProperty, BooleanProperty
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from View.Managers.notification_manager import NotificationManager
from View.Managers.http_manager import HttpManager


class Content(MDBoxLayout):
    """ Widget for displaying content of the dialog box (replying to messages). """
    pass


class MessagesScreenView(MDScreen):
    """ Screen displaying all registered customers. """
    data_tables = ObjectProperty(None)
    selected = ListProperty()
    dialog = ObjectProperty(None)
    checked = BooleanProperty(False)
    data = ObjectProperty()

    def __init__(self, **kwargs):
        super(MessagesScreenView, self).__init__(**kwargs)
        self.notification_manager = NotificationManager()

    def on_parent(self, widget, parent):
        self.data = self.manager.app.data
        self.data_tables = MDDataTable(
            size_hint=(1, .8),
            pos_hint={'top': .9, 'center_x': .5},
            use_pagination=True,
            rows_num=8,
            check=True,
            column_data=[
                ("Name", dp(50)),
                ("Email", dp(60)),
                ("Phone", dp(50)),
                ("Text Message", dp(100)),
                ("Date", dp(40)),
                ("ID", dp(10))

            ],
            row_data=[
                (item.get('name'),
                 ("email", [255 / 256, 165 / 256, 0, 1], item.get('mail')),
                 ("phone", [255 / 256, 165 / 256, 0, 1], item.get('phone')),
                 ("message", [255 / 256, 165 / 256, 0, 1],
                  textwrap.shorten(item.get('text_message'), width=30, placeholder='...')),
                 item.get('sent_on'),
                 item.get('id')) for item in self.data],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
            padding=dp(15),
            height=dp(25)
        )

        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)
        self.add_widget(self.data_tables)

    def on_row_press(self, instance_table, instance_row):
        """ Called when a table row is clicked. """
        if instance_row.index % 6 == 3:  # Works only on text message column
            index = instance_row.index // 6
            self.notification_manager.notify(self.data[index]['text_message'], duration=7)

    def on_check_press(self, instance_table, current_row):
        """ Called when the check-box in the table row is checked. """
        if current_row in self.selected:
            self.selected.remove(current_row)
        else:
            self.selected.append(current_row)
        if len(instance_table.get_row_checks()) > 1:
            self.notification_manager.notify("You can check just one row!", background=[1, 0, 0, .7])
            return

    def reply(self, obj):
        """ Sending reply emails! """
        if len(self.data_tables.get_row_checks()) > 1:
            self.notification_manager.notify("You can check just one row!", background=[1, 0, 0, .7])
            return
        title = self.dialog.content_cls.ids.title.text
        content = self.dialog.content_cls.ids.content.text
        if not title or not content:
            self.notification_manager.notify("Please fill out all fields.", background=[1, 0, 0, .7])
            return
        message_id = self.selected[0][-1]
        body = JSONEncoder().encode({'message': message_id, 'content': content, 'title': title})
        HttpManager().send_reply(self.success, self.failure, body, self.manager.app.token)

    def open_dialog(self):
        if len(self.selected) < 1:
            self.notification_manager.notify(text='Please check message to send an answer.')
            return
        elif len(self.selected) > 1:
            self.notification_manager.notify("You can check just one row!", background=[1, 0, 0, .7])
            return
        else:
            self.dialog = MDDialog(title="Send a reply:", type="custom", content_cls=Content(),
                                   buttons=[
                                       MDFillRoundFlatButton(text="Close", on_press=self.close),
                                       MDFillRoundFlatButton(text="Send", on_press=self.reply)])
        self.dialog.open()

    def success(self, result):
        self.notification_manager.notify(result, background=[0, 1, 0, .7])
        self.dialog.dismiss()

    def failure(self, result):
        self.notification_manager.notify(result, background=[1, 0, 0, .7])
        self.dialog.dismiss()

    def close(self, obj):
        self.dialog.dismiss()

    def back(self):
        self.manager.switch_screen('main')
