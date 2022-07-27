from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout


class OrdersScreenView(MDScreen):
    """ Screen displaying all confirmed orders. """
    recycleView = ObjectProperty(None)
    orders = ListProperty()

    def on_parent(self, widget, parent):
        dict_comprehension = [{
            'primary_data': customer['customer'],
            'secondary_data': customer['product'] + ' - Phone: ' + customer['phone'],
            'tertiary_data': 'Shipped: ' + str(customer['is_shipped']) + ' - message: ' + customer['message']
        }
            for customer in self.orders]
        self.recycleView.viewclass.data = self.orders
        self.recycleView.data = dict_comprehension


class OrdersDataWidget(MDBoxLayout):
    orientation = 'vertical'
    primary_data = StringProperty("")
    secondary_data = StringProperty("")
    tertiary_data = StringProperty("")
