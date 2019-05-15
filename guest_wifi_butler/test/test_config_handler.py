import os
from mock import patch
from unittest import TestCase
from guest_wifi_butler import script_location
from guest_wifi_butler.config.config_handler import ConfigHandler


class TestConfigHandler(TestCase):
    self_location = os.path.dirname(__file__)
    data_dir = os.path.join(self_location, 'data')
    dummy_config = os.path.join(data_dir, 'dummy_config.ini')

    @patch('os.path.exists')
    @patch('os.mkdir')
    @patch('os.access')
    def test_read_config_general(self, access_mock, mkdir_mock, path_exists_mock):
        path_exists_mock.return_value = False

        config = ConfigHandler(TestConfigHandler.dummy_config)

        expected_config_directory = os.path.join(script_location, 'kohl/meise')
        assert config.temp_directory == expected_config_directory, 'Could not read temp_directory from config'

        mkdir_mock.assert_any_call(expected_config_directory)
        access_mock.assert_any_call(expected_config_directory, os.W_OK)

    @patch('os.path.exists')
    @patch('os.mkdir')
    @patch('os.access')
    def test_read_config_wifi(self, access_mock, mkdir_mock, path_exists_mock):
        config = ConfigHandler(TestConfigHandler.dummy_config)

        assert config.ssid == 'dummy ssid', 'Could not read wifi ssid from config'
        assert config.encryption == 'WPA', 'Could not read wifi encryption from config'
        assert config.passphrase_length == 15, 'Could not read wifi passphrase length from config'
        assert config.update_passphrase_time == '04:00', 'Could not read wifi update passphrase time from config'
        assert config.seconds_to_gallery == 10, 'Could not read wifi seconds to gallery from config'

    @patch('os.path.exists')
    @patch('os.mkdir')
    @patch('os.access')
    def test_read_config_ios_config_server(self, access_mock, mkdir_mock, path_exists_mock):
        path_exists_mock.return_value = False

        config = ConfigHandler(TestConfigHandler.dummy_config)

        assert config.public_domain == 'domain.dummy', 'Could not read ios config server public domain from config'
        assert config.public_protocol == 'https', 'Could not read ios config server public protocol from config'
        assert config.public_port == 99999, 'Could not read ios config server public port from config'
        assert config.listen_port == 88888, 'Could not read ios config server listen port from config'
        assert config.listen_address == '256.256.256.256', 'Could not read ios config server listen address from config'
        assert config.identifier == 'dummy.domain'

        expected_config_directory = os.path.join(script_location, 'dummy/ios')
        assert config.config_directory == expected_config_directory, 'Could not read ios config server config directory from config'
        mkdir_mock.assert_any_call(expected_config_directory)
        access_mock.assert_any_call(expected_config_directory, os.W_OK)

    @patch('os.path.exists')
    @patch('os.mkdir')
    @patch('os.access')
    def test_read_config_gallery(self, access_mock, mkdir_mock, path_exists_mock):
        path_exists_mock.return_value = False

        config = ConfigHandler(TestConfigHandler.dummy_config)

        assert config.image_display_seconds == 10, 'Could not read gallery image display seconds from config'

        expected_image_directory = os.path.join(
            script_location, 'dummy/images')
        assert config.image_directory == expected_image_directory, 'Could not read gallery image directory from config'
        mkdir_mock.assert_any_call(expected_image_directory)
        access_mock.assert_any_call(expected_image_directory, os.W_OK)

    @patch('os.path.exists')
    @patch('os.mkdir')
    @patch('os.access')
    def test_read_config_gallery(self, access_mock, mkdir_mock, path_exists_mock):
        access_mock.return_value = False

        with self.assertRaises(OSError) as context:
            ConfigHandler(TestConfigHandler.dummy_config)

        self.assertIn('Permission error. Cannot write to', str(context.exception))
