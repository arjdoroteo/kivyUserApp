from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager


class myScreen(ScreenManager):
    name = ObjectProperty(None)

    def btn(self):
        print(self.name.text)
        pass


class AntiflameApp(MDApp):
    def build(self):
        Window.size = [450, 800]
        return myScreen()


if __name__ == "__main__":
    AntiflameApp().run()
