from pydoc import plain
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
import time


class AntiflameApp(MDApp):
    dialog = None
    cluster = MongoClient(
        'mongodb+srv://test1:123@cluster0.hfj9h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = cluster['Flame']
    collection = db['arjdoroteo']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.decryption, 2)

    def build(self):
        Window.size = [450, 800]
        return

    def showDialog(self, dialogMessage):
        Clock.unschedule(self.event)
        if not self.dialog:
            self.dialog = MDDialog(
                title='Emergency',
                text=dialogMessage,
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

    def pymongo(self):
        dataList = []
        results = self.collection.find().sort('_id', -1).limit(1)
        for result in results:
            temp = str(result['Temperature'])
            dataList.append(temp)
            co = str(result['CO'])
            dataList.append(co)
            lpg = str(result['LPG'])
            dataList.append(lpg)
            cipherText = result['User Info']
            dataList.append(cipherText)

        temp_limit = 125
        co_limit = 100
        lpg_limit = 10000

        if float(temp) >= temp_limit:
            self.showDialog(
                'Your temperature is too high!\n Temperature: ' + temp + 'C')
        elif float(co) >= co_limit:
            self.showDialog('CO values are too high!\n CO: ' + co + 'PPM')
        elif float(lpg) >= lpg_limit:
            self.showDialog('LPG values are too high!\n LPG: ' + lpg + 'PPM')

        return dataList

    def displayData(self, dt):
        dataList = self.pymongo()
        self.root.ids.temp.text = dataList[0] + ' C'
        self.root.ids.co.text = dataList[1] + ' PPM'
        self.root.ids.lpg.text = dataList[2] + ' PPM'

    def decryption(self, dt):
        dataList = self.pymongo()
        cipherText = dataList[3]

        with open('cipher_file', 'rb') as c_file:
            key = c_file.read(32)
            iv = c_file.read(16)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plainText = unpad(cipher.decrypt(cipherText), AES.block_size)

        stringText = plainText.decode('ascii')
        user_info_list = stringText.split(",")
        self.root.ids.userinfo.text = user_info_list[0]
        print(user_info_list)
        self.event = Clock.schedule_interval(self.displayData, 10)


if __name__ == "__main__":
    AntiflameApp().run()
