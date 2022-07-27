from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from View.Managers.http_manager import http_manager
from View.Managers.notification_manager import NotificationManager


class PrefilledForm(MDBoxLayout):
    pass


class ProductsWidget(MDBoxLayout):
    token = StringProperty()
    data = ListProperty()  # Holding list of available products
    dialog_box = ObjectProperty()  # Box for editing single product
    orientation = 'vertical'
    primary_data = StringProperty("")
    secondary_data = StringProperty("")
    tertiary_data = StringProperty("")
    name = StringProperty()  # Values of a single product used to populate dialog box (name, price and description)
    price = NumericProperty()
    description = StringProperty()

    def __init__(self, **kwargs):
        super(ProductsWidget, self).__init__(**kwargs)
        self.http_manager = http_manager
        self.notifier = NotificationManager()

    def edit_data(self, primary_data, token):
        self.token = token
        product_id = int(primary_data.split('-')[1])
        for product in self.data:
            if product['id'] == product_id:
                self.name = product['name']
                self.price = product['price']
                self.description = product['description']
        self.dialog_box = MDDialog(title="Edit Product:",
                                   type="custom",
                                   content_cls=PrefilledForm(),
                                   buttons=[
                                       MDFlatButton(text="DELETE", theme_text_color="Custom", on_press=self.delete),
                                       MDFlatButton(text="CANCEL", theme_text_color="Custom",
                                                    on_press=lambda x: self.dialog_box.dismiss()),
                                       MDFlatButton(text="SAVE", theme_text_color="Custom", on_press=self.save)
                                   ]
                                   )
        self.dialog_box.content_cls.ids.name.text = self.name
        self.dialog_box.content_cls.ids.description.text = self.description
        self.dialog_box.content_cls.ids.price.text = str(round(self.price, 2))
        self.dialog_box.product_id = product_id
        self.dialog_box.open()

    def save(self, widget):
        body = {
            'id': self.dialog_box.product_id,
            'name': self.dialog_box.content_cls.ids.name.text,
            'description': self.dialog_box.content_cls.ids.description.text,
            'price': self.dialog_box.content_cls.ids.price.text,
            'present': self.dialog_box.content_cls.ids.present.active
        }
        self.http_manager.edit_product(body=body, token=self.token)
        self.notifier.notify('Changes are saved!', background=[0, 1, 0, .65])
        self.dialog_box.dismiss()

    def delete(self, widget):
        self.http_manager.delete_product(product_id=self.dialog_box.product_id, token=self.token)
        self.notifier.notify('Item is deleted!', background=[1, 0, 0, .65])
        self.dialog_box.dismiss()


class ProductsScreenView(MDScreen):
    products = ListProperty()
    recycle_view = ObjectProperty()

    def data_from_dataset(self):
        dict_comprehension = [{
            'primary_data': product['name'] + '-' + str(product['id']),
            'secondary_data': 'Price: ' + str(product['price']),
            'tertiary_data': 'Edit'
        }
            for product in self.products]
        self.recycle_view.data = dict_comprehension
        return dict_comprehension

    def refresh_recycle_view(self):
        self.ids.recycle_view.data = self.data_from_dataset()
        self.ids.recycle_view.refresh_from_data()

    def on_enter(self, *args):
        self.data_from_dataset()
        self.recycle_view.viewclass.data = self.products
