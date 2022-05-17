from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import pymongo
from pymongo import MongoClient
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton


class AntiflameApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.decryption)
        self.event = Clock.schedule_interval(self.pymongo, 5)

    def build(self):
        Window.size = [450, 800]
        return

    def showDialog(self, temp, co, lpg):
        Clock.unschedule(self.event)
        if not self.dialog:
            self.dialog = MDDialog(
                title='Emergency',
                text='Limit Reached! Please check your system.',
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.close_dialog
                    )
                ]
            )
        self.dialog.open()
        print(temp, co, lpg)
        Clock.stop_clock()

    def close_dialog(self, obj):
        self.event()
        self.dialog.dismiss()

    def pymongo(self, dt):
        cluster = MongoClient(
            'mongodb+srv://test1:123@cluster0.hfj9h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        db = cluster['Flame']
        collection = db['arjdoroteo']
        results = collection.find().sort('_id', -1).limit(1)
        for result in results:
            temp = str(result['Temperature'])
            co = str(result['CO'])
            lpg = str(result['LPG'])

        self.root.ids.temp.text = temp + ' C'
        self.root.ids.co.text = co + ' PPM'
        self.root.ids.lpg.text = lpg + ' PPM'

        temp_limit = 125
        co_limit = 100
        lpg_limit = 10000

        if float(temp) >= temp_limit or float(co) >= co_limit or float(lpg) >= lpg_limit:
            self.showDialog(temp, co, lpg)
        else:
            pass

    def decryption(self, dt):
        cluster = MongoClient(
            'mongodb+srv://test1:123@cluster0.hfj9h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        db = cluster['Flame']
        collection = db['arjdoroteo']
        results = collection.find().sort('_id', -1).limit(1)
        for result in results:
            cipherText = result['User Info']

        with open('cipher_file', 'rb') as c_file:
            key = c_file.read(32)
            iv = c_file.read(16)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plainText = unpad(cipher.decrypt(cipherText), AES.block_size)

        self.root.ids.userinfo.text = str(plainText)


if __name__ == "__main__":
    AntiflameApp().run()
