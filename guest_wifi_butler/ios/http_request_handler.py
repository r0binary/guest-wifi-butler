import SimpleHTTPServer
import urllib
import os
import posixpath
from guest_wifi_butler.config.config_handler import ConfigHandler


class HTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = ConfigHandler().config_directory
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    def guess_type(self, path):
        _base, ext = posixpath.splitext(path)
        ext = ext.lower()
        if ext == '.mobileconfig':
            return 'application/x-apple-aspen-config'
        else:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.guess_type(self, path)
