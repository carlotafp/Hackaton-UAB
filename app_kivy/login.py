from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import requests

Window.keyboard_anim_argbs = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

class Ui(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"
        Builder.load_file('design.kv')
        self.url = "https://hackathon-24-dedef-default-rtdb.europe-west1.firebasedatabase.app/"
        self.key = "GLG7U55HoLUl3z3bODHAaNMKQU8G73sCTb5Lp8dz"
        return Ui()

    # def change_font(self):
    #     if self.font_type == 'fonts/Roboto-Regular.ttf':
    #         self.font_type = 'fonts/Roboto-Bold.ttf'
    #     else:
    #         self.font_type = 'fonts/Roboto-Regular.ttf'
    
    def login_data(self):
        userx = self.root.ids.user.text
        passwordx = self.root.ids.password.text
        state = False
        data = requests.get(self.url + "?auth=" + self.key)

        for key, value in data.json().items():
            user_reg = value["User"]
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
        state = "dades erronies"
        userx = self.root.ids.new_user.text
        password_one = self.root.ids.new_password.text
        password_two = self.root.ids.new_password_two.text

        data = requests.get(self.url + "?autn=" + self.key)

        if password_one != password_two:
            state = "LEs contrassenyes no coïncideixen"
        elif len(userx) <= 4:
            state = "Nom molt curt"
        elif password_one == password_two and len(password_two) <= 4:
            state = "Contrasenya molt curta"
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

