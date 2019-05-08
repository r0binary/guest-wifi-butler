import pyqrcode
import os

BLACK = (0, 0, 0, 255)
GREY = (136, 136, 136, 255)
WHITE = (255, 255, 255, 255)


class WifiQrGenerator(object):

    ANDROID_MAGIC_STRING_TEMPLATE = 'WIFI:T:%s;S:%s;P:%s;H:false;'
    WINDOWS_MAGIC_STRING_TEMPLATE = 'WIFI;T:%s;S:%s;P:%s;H:false;'

    def __init__(self, temp_directory):
        self.temp_directory = temp_directory

    def generate_android(self, encryption_method, ssid, passphrase):
        image_filename = os.path.join(self.temp_directory, 'android.png')
        magic_string = WifiQrGenerator.ANDROID_MAGIC_STRING_TEMPLATE % (
            encryption_method, ssid, passphrase)
        qrcode = pyqrcode.create(magic_string)
        qrcode.png(image_filename, scale=5,
                   module_color=GREY, background=BLACK)

    def generate_windows(self, encryption_method, ssid, passphrase):
        image_filename = os.path.join(self.temp_directory, 'windows.png')
        magic_string = WifiQrGenerator.WINDOWS_MAGIC_STRING_TEMPLATE % (
            encryption_method, ssid, passphrase)
        qrcode = pyqrcode.create(magic_string)
        qrcode.png(image_filename, scale=5,
                   module_color=GREY, background=BLACK)

    def generate_ios(self, config_uri):
        image_filename = os.path.join(self.temp_directory, 'ios.png')
        qrcode = pyqrcode.create(config_uri)
        qrcode.png(image_filename, scale=5,
                   module_color=GREY, background=BLACK)
