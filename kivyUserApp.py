import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class myGrid(Widget):
    name = ObjectProperty(None)
    email = ObjectProperty(None)

    def submitbtn(self):
        print('Name: ', self.name.text, 'Email: ', self.email.text)
class FlameApp(App):

    def build(self):
        
        return myGrid()

if __name__ == "__main__":
    FlameApp().run()
