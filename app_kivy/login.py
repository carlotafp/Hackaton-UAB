from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
import requests
from troba_tren import troba_tren

class Ui(ScreenManager):
    selected_object = StringProperty('')
    selected_origin = StringProperty('')
    selected_destination = StringProperty('')
    selected_traveler_type = StringProperty('')

class MainApp(MDApp):
    font_type = StringProperty('HelveticaNeue-Medium.otf')

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightGreen"
        self.menu_items = [
            {"text": "Plaça Catalunya"}, {"text": "Provença"}, {"text": "Gràcia"},
            {"text": "Sant Gervasi"}, {"text": "Muntaner"}, {"text": "La Bonanova"},
            {"text": "Les Tres Torres"}, {"text": "Sarrià"}, {"text": "Peu del Funicular"},
            {"text": "Baixador de Vallvidrera"}, {"text": "Les Planes"}, {"text": "La Floresta"},
            {"text": "Valldoreix"}, {"text": "Sant Cugat Centre"}, {"text": "Volpelleres"},
            {"text": "Sant Joan"}, {"text": "Bellaterra"}, {"text": "Universitat Autònoma"},
            {"text": "Sant Quirze"}, {"text": "Can Feu | Gràcia"}, {"text": "Sabadell Plaça Major"},
            {"text": "La Creu Alta"}, {"text": "Sabadell Nord"}, {"text": "Sabadell Parc del Nord"}
        ]

        self.menu_items2 = [
            {"text": "Cadira de rodes"}, {"text": "Embarassada"}, {"text": "Lisiat/da"},
            {"text": "3a Edat"}, {"text": "Família"},{"text": "Cotxet"}]

        self.dropdown_menus = {}
        self.dropdown_menus2 = {}

        Builder.load_file('design.kv')
        self.url = "https://hackathon2024-e4b02-default-rtdb.europe-west1.firebasedatabase.app/.json"
        self.key = "AR291WVNaDnDjXWMnwBPOhwhbZOPCElipxPS3Wu8"

        return Ui()

    def change_font(self):
        if self.font_type == 'HelveticaNeue-Medium.otf':
            self.font_type = 'OpenDyslexic-Regular.otf'
        else:
            self.font_type = 'HelveticaNeue-Medium.otf'
        for screen in self.root.screens:
            for widget in screen.walk():
                if hasattr(widget, 'font_name'):
                    widget.font_name = self.font_type

    def menu_open(self, button, category):
        if button in self.dropdown_menus:
            menu_items = self.dropdown_menus[button]
        else:
            if category == 'origin':
                menu_items = [
                    {
                        "viewclass": "OneLineListItem",
                        "text": item["text"],
                        "on_release": lambda x=item["text"]: self.option_selected(x, 'origin'),
                    } for item in self.menu_items
                ]
            elif category == 'destination':
                menu_items = [
                    {
                        "viewclass": "OneLineListItem",
                        "text": item["text"],
                        "on_release": lambda x=item["text"]: self.option_selected(x, 'destination'),
                    } for item in self.menu_items
                ]
            self.dropdown_menus[button] = menu_items

        self.open_dropdown(button, menu_items)

    def menu_open2(self, button):
        if button in self.dropdown_menus2:
            menu_items = self.dropdown_menus2[button]
        else:
            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": item["text"],
                    "on_release": lambda x=item["text"]: self.option_selected(x, 'traveler_type'),
                } for item in self.menu_items2
            ]
            self.dropdown_menus2[button] = menu_items

        self.open_dropdown(button, menu_items)

    def open_dropdown(self, button, menu_items):
        if not hasattr(self, 'dropdown_menu'):
            self.dropdown_menu = {}

        if button not in self.dropdown_menu:
            self.dropdown_menu[button] = MDDropdownMenu(
                caller=button,
                items=menu_items,
                width_mult=4
            )

        self.dropdown_menu[button].open()

    def option_selected(self, option, category):
        if category == 'origin':
            self.root.selected_origin = option
        elif category == 'destination':
            self.root.selected_destination = option
        elif category == 'traveler_type':
            self.root.selected_traveler_type = option

    def show_selected_object(self):
        if self.root.selected_origin and self.root.selected_destination and self.root.selected_traveler_type:
            tren = troba_tren(self.root.selected_origin, self.root.selected_destination, self.root.selected_traveler_type)
            self.root.selected_object = str(tren)
        else:
            self.root.selected_object = "Seleccioneu totes les opcions"

    def login_data(self):
        userx = str(self.root.ids.user.text)
        passwordx = self.root.ids.password.text
        state = False
        data = requests.get(self.url + "?auth=" + self.key)
        for key, value in data.json().items():
            user_reg = str(value["User"])
            password_reg = value["Password"]

            if userx == user_reg:
                if passwordx == password_reg:
                    state = True
                    self.root.ids.signal_login.text = ""
                    self.root.ids.user.text = ""
                    self.root.ids.password.text = ""
                else:
                    self.root.ids.signal_login.text = "Contrasenya incorrecta"
                    self.root.ids.user.text = ""
                    self.root.ids.password.text = ""
            else:
                self.root.ids.signal_login.text = "Usuari incorrecte"
                self.root.ids.user.text = ""
                self.root.ids.password.text = ""

        return state

    def register_data(self):
        state = "wrong data"
        userx = self.root.ids.new_user.text
        password_one = self.root.ids.new_password.text
        password_two = self.root.ids.new_password_two.text

        data = requests.get(self.url + "?auth=" + self.key)

        if password_one != password_two:
            state = "Les contrassenyes no coïncideixen"
        elif len(userx) <= 4:
            state = "Nom molt curt"
        elif password_one == password_two and len(password_two) <= 4:
            state = "Contrassenya molt curta"
        else:
            for key, value in data.json().items():
                user = value["User"]
                if user == userx:
                    state = "Aquest usuari ja existeix"
                    break
            if user != userx:
                state = "Registre correcte"
                send_data = {userx: {"User": userx, "Password": password_one}}
                requests.patch(url=self.url, json=send_data)
                self.root.ids.signal_register.text = state

        self.root.ids.signal_register.text = state
        self.root.ids.new_user.text = ""
        self.root.ids.new_password.text = ""
        self.root.ids.new_password_two.text = ""
        return state

    def clear_signal(self):
        self.root.ids.signal_register.text = ""
        self.root.ids.signal_login.text = ""

if __name__ == "__main__":
    MainApp().run()
