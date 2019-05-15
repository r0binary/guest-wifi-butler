from string import Template
from uuid import uuid4
from guest_wifi_butler import script_location
import os


class HostapdConfigBuilder:
    def __init__(self, config_filepath):
        self.__config_filepath = config_filepath

    def generate(self, ssid, passphrase):
        config_in_filename = 'hostapd.conf.in'
        config_in_filepath = os.path.join(
            script_location, 'data', config_in_filename)

        with open(config_in_filepath) as config_in_file, open(self.__config_filepath, 'w') as config_file:
            config_template = Template(config_in_file.read())
            config = config_template.substitute(
                ssid=ssid, passphrase=passphrase)
            config_file.write(config)
