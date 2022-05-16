from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import pymongo
from pymongo import MongoClient
from kivy.clock import Clock


class AntiflameApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.decryption)
        Clock.schedule_interval(self.pymongo, 5)

    def build(self):
        Window.size = [450, 800]
        return

    def pymongo(self, dt):
        cluster = MongoClient(
            'mongodb+srv://test1:123@cluster0.hfj9h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        db = cluster['Flame']
        collection = db['arjdoroteo']
        results = collection.find().sort('_id', -1).limit(1)
        for result in results:
            self.root.ids.temp.text = str(result['Temperature']) + ' C'
            self.root.ids.co.text = str(result['CO']) + ' PPM'
            self.root.ids.lpg.text = str(result['LPG']) + ' PPM'

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
