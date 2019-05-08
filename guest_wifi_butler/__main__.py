import threading
import subprocess
import time
import schedule
import atexit
import shutil
import random
import string
import sys
from guest_wifi_butler.ui.app import GuestWifiButlerApp
from guest_wifi_butler.wifi_qr_generator import WifiQrGenerator
from guest_wifi_butler.config.config_handler import ConfigHandler
from guest_wifi_butler.config.hostapd_config_builder import HostapdConfigBuilder
from guest_wifi_butler.ios.configuration_profile_creator import iOSConfigurationProfileCreator
from guest_wifi_butler.ios.configuration_profile_server import iOSConfigurationProfileServer


def hostapd_restart():
    sys.stdout.write('Restarting Hostapd...')
    assert subprocess.call('/usr/sbin/service hostapd stop'.split(' '),
                           shell=False) == 0, 'Cannot stop Hostapd service'
    time.sleep(8)
    assert subprocess.call('/usr/sbin/service hostapd start'.split(' '),
                           shell=False) == 0, 'Cannot start Hostapd service'
    sys.stdout.write(' Done\n')


def update_wifi_information(config):
    passphrase = generate_passphrase(config.passphrase_length)

    ios_config_creator = iOSConfigurationProfileCreator(
        config.config_directory)
    config_filename = ios_config_creator.generate(config.ssid,
                                                  passphrase,
                                                  config.identifier)
    config_uri = '%s://%s:%d/%s' % (config.public_protocol,
                                    config.public_domain,
                                    config.public_port,
                                    config_filename)
    # Is the mime types set correctly?

    wifi_qr_generator = WifiQrGenerator(config.temp_directory)
    wifi_qr_generator.generate_android(
        config.encryption, config.ssid, passphrase)
    wifi_qr_generator.generate_windows(
        config.encryption, config.ssid, passphrase)
    wifi_qr_generator.generate_ios(config_uri)

    HostapdConfigBuilder(
        '/etc/hostapd/hostapd.conf').generate(config.ssid, passphrase)
    hostapd_restart()
    return passphrase


def start_task_scheduler():
    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run)
    scheduler_thread.daemon = True
    scheduler_thread.start()


def generate_passphrase(length):
    allowed_characters = string.letters + string.digits
    return ''.join(random.choice(allowed_characters) for _ in range(length))


def main():
    config = ConfigHandler()
    passphrase = update_wifi_information(config)
    app = GuestWifiButlerApp(config, passphrase)

    server = iOSConfigurationProfileServer()
    server.startServer(config.listen_address, config.listen_port)

    def run_update_wifi():
        passphrase = update_wifi_information(config)
        app.update_wifi_information(passphrase)

    schedule.every().day.at(config.update_passphrase_time).do(run_update_wifi)
    start_task_scheduler()

    def remove_temp_directory():
        shutil.rmtree(config.temp_directory)

    atexit.register(remove_temp_directory)

    app.run()


if __name__ == "__main__":
    main()
