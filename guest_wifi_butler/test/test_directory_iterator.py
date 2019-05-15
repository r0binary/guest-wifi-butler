from mock import patch
from unittest import TestCase
from guest_wifi_butler.directory_iterator import DirectoryIterator


class TestDirectoryIterator(TestCase):

    @patch('guest_wifi_butler.directory_iterator.glob')
    def test_read_empty_directory(self, glob_mock):
        glob_mock.return_value = []

        iter = DirectoryIterator('empty_directory')

        assert iter.__next__() == None

    @patch('guest_wifi_butler.directory_iterator.glob')
    def test_read_image_directory(self, glob_mock):
        glob_mock.return_value = ['image1', 'image2', 'image3']

        iter = DirectoryIterator('image_directory')

        assert iter.__next__() == 'image1'
        assert iter.__next__() == 'image2'
        assert iter.__next__() == 'image3'
        assert iter.__next__() == 'image1'

    @patch('guest_wifi_butler.directory_iterator.glob')
    def test_read_image_directory_iterator(self, glob_mock):
        glob_mock.return_value = []

        iter = DirectoryIterator('empty_directory')

        assert iter.__iter__() == iter
