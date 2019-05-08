from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from guest_wifi_butler.directory_iterator import DirectoryIterator


class Gallery(Screen):
    gallery_image = ObjectProperty(None)

    def __init__(self, image_directory, image_display_seconds, *args, **kwargs):
        Screen.__init__(self, *args, **kwargs)
        self.__image_iterator = DirectoryIterator(image_directory)
        Clock.schedule_interval(self.update, image_display_seconds)
        self.update()

    def update(self, dt=None):
        self.gallery_image.source = self.__image_iterator.next()
