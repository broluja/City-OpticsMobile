from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout


class CustomersScreenView(MDScreen):
    """ Screen displaying all registered customers. """
    recycle_view_customers = ObjectProperty(None)
    customers = ListProperty()  # Holding all registered customers, generated on pre-enter

    def data_from_dataset(self):
        dict_comprehension = [{
            'primary_data': f'{customer["email"]} Phone: {str(customer["phone"])}',
            'secondary_data': f'Used discount: {str(customer["discount_used"])}',
            'tertiary_data': f'Code: {customer["code"]}'
        }
            for customer in self.customers]
        self.recycle_view_customers.data = dict_comprehension
        return dict_comprehension

    def refresh_recycle_view(self):
        self.ids.recycle_view_customers.data = self.data_from_dataset()
        self.ids.recycle_view_customers.refresh_from_data()

    def on_enter(self, *args):
        self.data_from_dataset()
        self.recycle_view_customers.viewclass.data = self.customers


class CustomersDataWidget(MDBoxLayout):
    orientation = 'vertical'
    primary_data = StringProperty("")
    secondary_data = StringProperty("")
    tertiary_data = StringProperty()
