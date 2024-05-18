from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import requests
from kivy.properties import StringProperty

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

class Ui(ScreenManager):
    pass

class MainApp(MDApp):
    font_type = StringProperty('HelveticaNeue-Medium.otf')
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
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
                send_data = {userx: {"User":userx, "Password":password_one}}
                requests.patch(url = self.url, json = send_data)
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

