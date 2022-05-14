from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager


class AntiflameApp(MDApp):

    def build(self):
        Window.size = [450, 800]
        return

    def btn(self):
        print(self.root.ids.name.text)


if __name__ == "__main__":
    AntiflameApp().run()
