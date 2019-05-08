from string import Template
from uuid import uuid4
from guest_wifi_butler import script_location
import os


class iOSConfigurationProfileCreator:
    def __init__(self, config_directory):
        self.__config_directory = config_directory

    def generate(self, ssid, passphrase, identifier):
        config_in_filename = 'template.mobileconfig.in'
        config_in_filepath = os.path.join(
            script_location, 'data', config_in_filename)
        config_filename = '%s.mobileconfig' % passphrase
        config_filepath = os.path.join(
            self.__config_directory, config_filename)

        with open(config_in_filepath) as config_in_file, open(config_filepath, 'w') as config_file:
            config_template = Template(config_in_file.read())
            config = config_template.substitute(
                ssid=ssid,
                passphrase=passphrase,
                uuid=str(uuid4()),
                identifier=identifier
            )
            config_file.write(config)

        return config_filename
