from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import pymongo
from pymongo import MongoClient
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton


class CentralApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.decryptionUserInfo, 1)

    def build(self):

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
        Clock.stop_clock()

    def close_dialog(self, obj):
        self.event()
        self.dialog.dismiss()

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

    def compareData(self, data):
        temp_limit = 80
        co_limit = 25
        lpg_lower_limit = 150
        lpg_upper_limit = 2000

        temp = data[1]
        lpg = data[2]
        co = data[3]

        if float(temp) >= temp_limit:
            self.showDialog(
                'Your temperature is too high!\n \nTemperature: ' + str(temp) + 'C')
        elif float(co) >= co_limit:
            self.showDialog(
                'CO values are too high! Be careful of Carbon Monoxide Poisoning. Please check your system immediately\n\n CO: ' + str(co) + 'PPM')
        elif float(lpg) >= lpg_lower_limit and float(lpg) < lpg_upper_limit:
            self.showDialog(
                'Low levels of LPG detected, there may be a gas leak!\n LPG: ' + str(lpg) + ' PPM')

    def updateSidePanel(self, dt):

        data = self.pymongo()
        self.root.ids.userinfo.secondary_text = 'Temperature: ' + str(data[1]) + \
            ' C ' + 'LPG: ' + str(data[2]) + ' PPM'
        self.root.ids.userinfo.tertiary_text = 'CO: '+str(data[3]) + ' PPM'

        self.compareData(data)

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

        self.pin = MapMarkerPopup(lat=userInfoList[1], lon=userInfoList[2])
        self.root.ids.map.add_widget(self.pin)

        self.event = Clock.schedule_interval(self.updateSidePanel, 5)


if __name__ == "__main__":
    CentralApp().run()
