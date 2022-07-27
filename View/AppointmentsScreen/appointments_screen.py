from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout


class AppointmentsScreenView(MDScreen):
    """ Screen displaying all confirmed appointments. """
    recycleView = ObjectProperty(None)
    appointments = ListProperty()  # Holding list of all appointments, generated on pre-enter

    def on_parent(self, widget, parent):
        dict_comprehension = [{
            'primary_data': customer['name'],
            'secondary_data': 'Phone: ' + customer['phone'],
            'tertiary_data': 'Date: ' + customer['date'] + ' | Hour: ' + customer['hour']
        }
            for customer in self.appointments]
        self.recycleView.viewclass.data = self.appointments
        self.recycleView.data = dict_comprehension


class AppointmentDataWidget(MDBoxLayout):
    orientation = 'vertical'
    primary_data = StringProperty("")
    secondary_data = StringProperty("")
    tertiary_data = StringProperty("")
