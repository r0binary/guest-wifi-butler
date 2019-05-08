import pyqrcode
import os
from mock import MagicMock, patch
from guest_wifi_butler.wifi_qr_generator import WifiQrGenerator, BLACK, GREY


class TestWifiQrGenerator:

    def test_store_temp_directory_in_constructor(self):
        temp_directory = 'test_temp_directory'
        wifi_qr_generator = WifiQrGenerator(temp_directory)
        assert wifi_qr_generator.temp_directory == temp_directory, 'It should store the temp-directory'

    def test_generate_android_qr_string(self):
        with patch.object(pyqrcode, 'create', return_value=MagicMock()) as pyqrcode_create_mock:
            test_data = ('test_encryption_method',
                         'test_ssid',
                         'test_passphrase')

            WifiQrGenerator('').generate_android(*test_data)

            expected_result = WifiQrGenerator.ANDROID_MAGIC_STRING_TEMPLATE % test_data
            pyqrcode_create_mock.assert_called_once_with(expected_result)

    def test_write_android_qr_code_as_png(self):
        temp_directory = 'test_temp_directory'
        pyqrcode_png_mock = MagicMock()

        with patch.object(pyqrcode, 'create', return_value=pyqrcode_png_mock):
            wifi_qr_generator = WifiQrGenerator(temp_directory)
            wifi_qr_generator.generate_android('', '', '')

            pyqrcode_png_mock.png.assert_called_once_with(
                os.path.join(temp_directory, 'android.png'), background=BLACK, module_color=GREY, scale=5)

    def test_generate_windows_qr_string(self):
        with patch.object(pyqrcode, 'create', return_value=MagicMock()) as pyqrcode_create_mock:
            test_data = ('test_encryption_method',
                         'test_ssid',
                         'test_passphrase')

            WifiQrGenerator('').generate_windows(*test_data)

            expected_result = WifiQrGenerator.WINDOWS_MAGIC_STRING_TEMPLATE % test_data
            pyqrcode_create_mock.assert_called_once_with(expected_result)

    def test_write_windows_qr_code_as_png(self):
        temp_directory = 'test_temp_directory'
        pyqrcode_png_mock = MagicMock()

        with patch.object(pyqrcode, 'create', return_value=pyqrcode_png_mock):
            wifi_qr_generator = WifiQrGenerator(temp_directory)
            wifi_qr_generator.generate_windows('', '', '')

            pyqrcode_png_mock.png.assert_called_once_with(
                os.path.join(temp_directory, 'windows.png'), background=BLACK, module_color=GREY, scale=5)

    def test_generate_ios_qr_string(self):
        with patch.object(pyqrcode, 'create', return_value=MagicMock()) as pyqrcode_create_mock:
            test_config_uri = 'https://testdomain.fake:443/test.config'

            WifiQrGenerator('').generate_ios(test_config_uri)

            pyqrcode_create_mock.assert_called_once_with(test_config_uri)

    def test_write_ios_qr_code_as_png(self):
        temp_directory = 'test_temp_directory'
        pyqrcode_png_mock = MagicMock()

        with patch.object(pyqrcode, 'create', return_value=pyqrcode_png_mock):
            wifi_qr_generator = WifiQrGenerator(temp_directory)
            wifi_qr_generator.generate_ios('')

            pyqrcode_png_mock.png.assert_called_once_with(
                os.path.join(temp_directory, 'ios.png'), background=BLACK, module_color=GREY, scale=5)
