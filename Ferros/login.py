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
        return Ui()