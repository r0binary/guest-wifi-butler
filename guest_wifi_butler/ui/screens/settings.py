from kivy.uix.screenmanager import Screen, SwapTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.image import Image
import os


class Settings(Screen):
    brightness = ObjectProperty(None)
    brigthness_dispay = StringProperty(None)

    def __init__(self, *args, **kwargs):
        Screen.__init__(self, *args, **kwargs)

    def update_brightness(self, *args):
        self.__update_brightness_display_label()
        self.adjust_brightness()

    def __update_brightness_display_label(self):
        self.brightness_display.text = '%d %%' % Settings.calculcate_brightness_percentage(
            self.brightness.value)

    def adjust_brightness(self):
        brightness_as_string = str(int(self.brightness.value))
        with open('/sys/class/backlight/rpi_backlight/brightness', 'w') as brightness_fp:
            brightness_fp.write(brightness_as_string)

    def read_current_brightness(self):
        with open('/sys/class/backlight/rpi_backlight/brightness', 'r') as brightness_fp:
            return max(brightness_fp.read().strip('\n'), 10)

    @staticmethod
    def calculcate_brightness_percentage(absolute_value):
        return int(absolute_value / 2.55)
