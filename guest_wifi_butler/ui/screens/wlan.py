from kivy.uix.screenmanager import Screen, SwapTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.image import Image


class WLAN(Screen):
    passphrase = StringProperty(None)
    android_qrcode = ObjectProperty(None)
    ios_qrcode = ObjectProperty(None)
    windows_qrcode = ObjectProperty(None)
    gallery_timer = ObjectProperty(None)

    def __init__(self, seconds_to_gallery, *args, **kwargs):
        Screen.__init__(self, *args, **kwargs)
        self.__seconds_to_gallery = seconds_to_gallery

    def update(self, passphrase, *args):
        self.passphrase = passphrase
        self.android_qrcode.reload()
        self.ios_qrcode.reload()
        self.windows_qrcode.reload()

    def on_enter(self):
        def switchToGalery(dt):
            self.manager.transition = SwapTransition(duration=3)
            self.manager.current = 'gallery'
        self.gallery_timer = Clock.schedule_once(
            switchToGalery, self.__seconds_to_gallery)
