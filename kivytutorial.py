import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout


class myGrid(FloatLayout):
    name = ObjectProperty(None)
    email = ObjectProperty(None)

    def submitbtn(self):
        print('Name: ', self.name.text, 'Email: ', self.email.text)


class TestApp(App):

    def build(self):

        return myGrid()


if __name__ == "__main__":
    TestApp().run()
