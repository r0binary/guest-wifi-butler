import os
from configparser import RawConfigParser
from guest_wifi_butler import script_location


DEFAULT_CONFIG = os.path.join(script_location, 'guest_wifi_config.ini')


class ConfigHandler:
    def __init__(self, config_filepath=DEFAULT_CONFIG):
        config = RawConfigParser(allow_no_value=True)
        config.read(config_filepath)

        self.temp_directory = self.__assertWritableDirectory(
            config.get('general', 'temp_directory'))

        self.ssid = config.get('wifi', 'ssid')
        self.encryption = config.get('wifi', 'encryption')
        self.passphrase_length = config.getint('wifi', 'passphrase_length')
        self.update_passphrase_time = config.get(
            'wifi', 'update_passphrase_time')
        self.seconds_to_gallery = config.getint(
            'wifi', 'seconds_to_gallery')

        self.public_domain = config.get('ios_config_server', 'public_domain')
        self.public_protocol = config.get(
            'ios_config_server', 'public_protocol')
        self.public_port = config.getint('ios_config_server', 'public_port')

        self.listen_port = config.getint('ios_config_server', 'listen_port')
        self.listen_address = config.get('ios_config_server', 'listen_address')
        self.config_directory = self.__assertWritableDirectory(
            config.get('ios_config_server', 'config_directory'))
        self.identifier = '.'.join(self.public_domain.split('.')[::-1])

        self.image_directory = self.__assertWritableDirectory(
            config.get('gallery', 'image_directory'))
        self.image_display_seconds = config.getint(
            'gallery', 'image_display_seconds')

    def __assertWritableDirectory(self, filepath):
        if not os.path.isabs(filepath):
            filepath = os.path.join(script_location, filepath)

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        if not os.access(filepath, os.W_OK):
            raise OSError('Permission error. Cannot write to %s' % filepath)

        return filepath
