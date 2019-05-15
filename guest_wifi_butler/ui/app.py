from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from guest_wifi_butler.ui.screens.wlan import WLAN
from guest_wifi_butler.ui.screens.gallery import Gallery
from guest_wifi_butler.ui.screens.settings import Settings


class GuestWifiButlerApp(App):
    def __init__(self, config, initial_passphrase, *args, **kwargs):
        App.__init__(self, *args, **kwargs)
        self.title = 'Guest WiFi Butler (inspired by Heise)'
        self.__screen_manager = ScreenManager()
        self.__config = config
        self.__initial_passphrase = initial_passphrase

    def build(self):
        self.__screen_manager.add_widget(
            Gallery(self.__config.image_directory, self.__config.image_display_seconds))
        self.__screen_manager.add_widget(
            WLAN(self.__config.seconds_to_gallery))
        self.update_wifi_information(self.__initial_passphrase)
        self.__screen_manager.add_widget(Settings())
        return self.__screen_manager

    def update_wifi_information(self, passphrase):
        wlan_widget = self.__screen_manager.get_screen('wlan')
        # We need to let Kivy call the update to be in the right context
        # else the image reload will produce weird results
        Clock.schedule_once(partial(wlan_widget.update, passphrase), 0)
