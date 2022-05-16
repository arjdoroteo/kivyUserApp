from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import pymongo
from pymongo import MongoClient
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker


class CentralApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.decryptionUserInfo)
        Clock.schedule_interval(self.decryptionUserInfo, 15)

    def build(self):

        return

    def pymongo(self):
        cluster = MongoClient(
            'mongodb+srv://test1:123@cluster0.hfj9h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        db = cluster['Flame']
        collection = db['arjdoroteo']
        results = collection.find().sort('_id', -1).limit(1)
        data = []
        for result in results:
            data.append(result['User Info'])
            data.append(result['Temperature'])
            data.append(result['LPG'])
            data.append(result['CO'])
        return data

    def decryptionUserInfo(self, dt):
        data = self.pymongo()
        cipherText = data[0]
        with open('cipher_file', 'rb') as c_file:
            key = c_file.read(32)
            iv = c_file.read(16)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plainText = unpad(cipher.decrypt(cipherText), AES.block_size)

        plainText = str(plainText)
        plainText = plainText[2:-1]
        userInfoList = plainText.split(',')

        self.root.ids.userinfo.text = str(userInfoList[0])
        userInfoList = plainText.split(',')

        self.root.ids.userinfo.text = str(userInfoList[0])
        self.root.ids.userinfo.secondary_text = str(data[1]) + \
            ' C ' + str(data[2]) + ' PPM'
        self.root.ids.userinfo.tertiary_text = str(data[3]) + ' PPM'


if __name__ == "__main__":
    CentralApp().run()
